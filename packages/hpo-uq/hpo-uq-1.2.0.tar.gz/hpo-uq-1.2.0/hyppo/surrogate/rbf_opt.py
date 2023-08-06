# System
import os
import copy
import math
import time
import logging

# External
import numpy
import numpy.matlib as npm
import scipy.spatial as scp
import pickle5 as pickle
#from pyDOE import *

# Local
from ..train import train_evaluation
from ..utils import extract_evals, check_surrogate_sample
from .phi import phi
from .InitialRBFMatrices import InitialRBFMatrices, UpdateRBFMatrices
from .ComputeRBF import ComputeRBF

def rbf(config,log_dir,loops,step,rank,xlow,xup,mult,names,
        maxshrinkparam=5,succtolerance=3,Ncand=500,default={},**kwargs):
    """
    Radial Basis Function based surrogate optimization algorithm.    

    Parameters
    ----------
    config : :class:`dict`
      Configuration dictionary object to be used when evaluating subsequent sample sets.
    log_dir : :class:`str`
      Relative path where log files are stored
    loops : :class:`int`
      Number of iterations to do surrogate modeling over.
    step : :class:`int`
      Current SLURM step
    rank : :py:class:`int`
      Current processor rank
    xlow : :class:`list` [ :class:`int` ]
      Lower boundaries of hyperparameters to evaluate.
    xup : :class:`list` [ :class:`int` ]
      Upper boundaries of hyperparameters to evaluate.
    mult : :class:`list` [ :class:`int` ]
      Scaling factor for each hyperparameter
    names : :class:`list` [ :class:`str` ]
      Name of each hyperparameter
    maxshrinkparam : :class:`int`
      Maximal number of shrinkage of standard deviation for normal distribution when generating the candidate points
    succtolerance : :class:`int`
      Success tolerance
    default : :class:`dict`
      Dictionary of default hyperparameter values
    """
    out_path = 'original'
    # Initialize RBF class
    rbf = ComputeRBF(**kwargs)
    # Tolerance parameters
    tolerance = 0.001 * numpy.min([xup-xlow for xup,xlow in zip(xup,xlow)]) * numpy.linalg.norm(numpy.ones((1, len(mult))))
    # Algorithm parameters -- delete stuff from here, not necessary for this problem
    sigma_stdev_default = 1 # integers
    sigma_stdev         = sigma_stdev_default # current mutation rate
    failtolerance       = max(5,len(mult))
    # Initializations
    shrinkctr           = 0 # number of times sigma_stdev was shrunk
    failctr             = 0 # number of consecutive unsuccessful iterations
    localminflag        = 0 # indicates whether or not xbest is at a local minimum
    succctr             = 0 # number of consecutive successful iterations
    #p                   = fvals[0, 0]
    valweight           = 1.25
    maxvalweight        = 1
    # Print out parameters for generational process
    logging.info('='*40)
    logging.info('RADIAL BASIS FUNCTION PARAMETERS')
    logging.info('-'*40)
    logging.info('Maximum shrinkage : {}'.format(maxshrinkparam))
    logging.info('Success tolerance : {}'.format(succtolerance))
    logging.info('='*40+'\n')
    # Loop through evaluations
    for iloop in range(loops):
        logging.info('='*40)
        logging.info('SURROGATE ITERATION {:>3} / {:<3}'.format(iloop+1,loops))
        logging.info('-'*40)
        if rank == 0:
            if localminflag != 0:
                break
            # Gather results, fit and save GP model
            samples, fvals, xbest, Fbest = get_fvals(log_dir)
            valweight -= 0.25
            if valweight<0:
                valweight = maxvalweight
            if iloop==0:
                # Build the surrogate - Determine pairwise distance between points
                PairwiseDistance = scp.distance.cdist(samples, samples, 'euclidean')
                # Build the surrogate - Initial RBF matrices
                PHI, P, pdim = InitialRBFMatrices(PairwiseDistance,samples,**kwargs)
            else:
                # update PHI matrix only if planning to do another iteration
                PHI, P = UpdateRBFMatrices(samples, PHI, P, PairwiseDistance, r=normval[0], **kwargs)
            # Initialize array with function values
            #fvals = numpy.asmatrix(numpy.zeros(fvals.shape))
            # number of new samples in an iteration
            #NumberNewSamples = min(data.nns,data.maxeval - data.m)
            # replace large function values by the median of all available function values
            #Ftransform = numpy.copy(numpy.asarray(data.Y)[0:data.m])
            #medianF = numpy.median(numpy.asarray(data.Y)[0:data.m])
            #Ftransform[Ftransform > medianF] = medianF
            # Fit the response surface - Compute RBF parameters
            a_part1 = numpy.concatenate((PHI, P), axis = 1)
            a_part2 = numpy.concatenate((numpy.transpose(P), numpy.zeros((pdim, pdim))), axis = 1)
            a = numpy.concatenate((a_part1, a_part2), axis = 0)
            eta = math.sqrt((1e-16) * numpy.linalg.norm(a, 1) * numpy.linalg.norm(a, numpy.inf))
            if fvals.shape[1]==1:
                coeff = numpy.linalg.solve((a + eta * numpy.eye(len(samples) + pdim)),
                                        numpy.concatenate((fvals[:,:1], numpy.zeros((pdim, 1))), axis = 0))
                # llambda is not a typo, lambda is a python keyword
                llambda = [coeff[0:len(samples)]]
                ctail = [coeff[len(samples): len(samples) + pdim]]
            else:
                a_inv   = numpy.linalg.inv(a + eta * numpy.eye(len(samples) + pdim))
                llambda = []
                ctail   = []
                for i in range(30): #This generates 30 different response surfaces using the CIs
                    indx  = numpy.random.choice(range(3),(len(samples),1))
                    rhs   = numpy.asmatrix([fvals[k,indx[k,0]] for k in range(len(samples))]).T
                    rhs   = numpy.concatenate((rhs,numpy.zeros((pdim,1))),axis=0)
                    coeff = numpy.matmul(a_inv,rhs)
                    llambda.append(coeff[0:len(samples)])
                    ctail.append(coeff[len(samples): len(samples)+pdim])
                llambda = llambda
                ctail   = ctail
            rbf.update(samples,llambda,ctail)
            save_model(log_dir,out_path,rbf)
            logging.info('Total of sample sets used : %i' % len(samples))
            logging.info('Best loss value so far    : %.5f' % Fbest)
            logging.info('-'*40)
            # Find next set of hyperparameters
            # Introduce candidate points  -- update later when number of nodes >1
            # CandPoint = numpy.asmatrix(data.val_list).T #this needs to be updated when we're 
            # create candidate point:
            # perturb xbest - local perturbations: 1 or 2 for parameters 1 and 2, 1 for parameters 3 and 4
            C1 = npm.repmat(xbest, Ncand, 1)
            R  = numpy.zeros((Ncand, samples.shape[1]))
            for ii in range(samples.shape[1]):
                R[:,ii]=numpy.ravel(numpy.random.randint(0,3,(Ncand,1))*numpy.random.choice(numpy.array([-1,1]),(Ncand,1)))
            CP = R + C1
            # Reflect outsiders over boundary to inside
            for ii in range(samples.shape[1]):
                vec_ii = CP[:, ii]
                adj_l = numpy.where(vec_ii < xlow[ii])
                vec_ii[adj_l[0]] = xlow[ii] + (xlow[ii] - vec_ii[adj_l[0]])
                adj_u = numpy.where(vec_ii > xup[ii])
                vec_ii[adj_u[0]] = xup[ii] - (vec_ii[adj_u[0]]-xup[ii])
                stillout_u = numpy.where(vec_ii > xup[ii])
                vec_ii[stillout_u[0]] = xlow[ii]
                stillout_l = numpy.where(vec_ii < xlow[ii])
                vec_ii[stillout_l[0]] = xup[ii]
                CP[:, ii] = copy.copy(vec_ii)
            # Generate second set of randomly generated points
            CR = numpy.zeros((Ncand, samples.shape[1]))
            for ii in range(samples.shape[1]):
                CR[:,ii]=numpy.ravel(numpy.random.randint(xlow[ii],xup[ii],(Ncand,1)))
            CandPoint = numpy.concatenate((CP,CR), axis = 0)#all candidate points
            CandValue, NormValue = rbf.fit(CandPoint)
            xselected, normval = Minimize_Merit_Function(CandPoint, CandValue, NormValue, fvals, tolerance, valweight)
            xselected = numpy.array(xselected,dtype=int)
            logging.info('Samples: %s' % xselected)
        else:
            logging.info('Surrogate modeling in progress...')
            while check_surrogate_sample(log_dir,step,iloop)==[]:
                continue
            xselected = check_surrogate_sample(log_dir,step,iloop)
            logging.info('Samples: %s' % xselected)
        # Execute training
        x_sc = [int(xselected[n])*mult[n] for n in range(samples.shape[1])]
        x_sc = {name:value for name,value in zip(names,x_sc)}
        x_sc = {**x_sc,**default}
        out_path = 'surrogate_%s' % ('_'.join(numpy.array(xselected,dtype=str)))
        Fselected = train_evaluation(x_sc,xselected,output=out_path,**config)
        logging.info('='*40+'\n')

#         if Fselected < Fbest:
#             if Fbest - Fselected > (1e-3)*math.fabs(Fbest):
#                 # "significant" improvement
#                 failctr = 0
#                 succctr = succctr + 1
#             else:
#                 failctr = failctr + 1
#                 succctr = 0
#             xbest = xselected
#             Fbest = Fselecteds
#             #data.best_Y = best_Y
#             #best_model = model
#         else:
#             failctr = failctr + 1
#             succctr = 0
#         check if algorithm is in a local minimum
#         shrinkflag = 1
#         if failctr >= failtolerance:
#            localminflag = 1
#         if succctr >= succtolerance:
#            sigma_stdev = min(2 * sigma_stdev, sigma_stdev_default)
#            succctr = 0

def Minimize_Merit_Function(CandPoint, CandValue, NormValue, fvals, tolerance, valueweight):
    if fvals.shape[1]>1:
        #CandValue = CandValue[:,0] #mean value computed for each candiate point of the rbf ensembles
        CandValue = CandValue[:,0]+2*CandValue[:,1] #mean + 2std  
    MinCandValue = numpy.amin(CandValue)
    MaxCandValue = numpy.amax(CandValue)
    if MinCandValue == MaxCandValue:
        ScaledCandValue = numpy.ones((CandValue.shape[0], 1))
    else:
        ScaledCandValue = (CandValue - MinCandValue) / (MaxCandValue - MinCandValue)
    CandMinDist = numpy.asmatrix(numpy.amin(NormValue, axis = 0)).T
    MaxCandMinDist = numpy.amax(CandMinDist)
    MinCandMinDist = numpy.amin(CandMinDist)
    if MaxCandMinDist == MinCandMinDist:
        ScaledCandMinDist = numpy.ones((CandMinDist.shape[0], 1))
    else:
        ScaledCandMinDist = (MaxCandMinDist - CandMinDist) / (MaxCandMinDist - MinCandMinDist)
    # compute weighted score for all candidates
    CandTotalValue = valueweight * ScaledCandValue + (1 - valueweight) * ScaledCandMinDist
    # assign bad scores to candidate points that are too close to already sampled points
    CandTotalValue[CandMinDist < tolerance] = numpy.inf
    MinCandTotalValue = numpy.amin(CandTotalValue)
    selindex = numpy.argmin(CandTotalValue)
    xselected = numpy.array(CandPoint[selindex, :])
    #print(xselected)
    normval = {}
    normval[0] = numpy.asmatrix((NormValue[:, selindex])).T
    return xselected, normval

def get_fvals(log_dir):
    """
    Extract results, fit and save GP model.
    """
    # Extract values
    samples, fvals, Fbest, xbest = extract_evals(log_dir)
    # Remove infinite losses
    idxs = numpy.argwhere(numpy.isinf(fvals[:,0]))
    if len(idxs)>0:
        samples = numpy.delete(samples,idxs[:,0],axis=0)
        fvals   = numpy.delete(fvals,idxs[:,0],axis=0)
    return samples, fvals, xbest, Fbest

def save_model(log_dir,out_path,rbf):
    """
    Save surrogate Radial Basis Function model
    """
    path = os.path.join(log_dir,'models',out_path)
    os.makedirs(path,exist_ok=True)
    with open(path+'/rbf_model.pkl','wb') as f:
        pickle.dump(rbf,f)
