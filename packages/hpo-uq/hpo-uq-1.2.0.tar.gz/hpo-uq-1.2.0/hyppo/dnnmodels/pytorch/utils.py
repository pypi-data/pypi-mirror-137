# System
import os
import time
import random
import logging
import importlib
from collections import OrderedDict
import numpy as np

# External
import torch
import numpy
import scipy
from scipy.stats import norm, median_abs_deviation
from scipy.integrate import quad
import matplotlib.pyplot as plt

def shape_and_size(data, n_classes=None, **kwargs):
    """
    Extract input/output shape and size. This function is used to determine
    the right dimension of both input and output data.
    
    Parameters
    ----------
    data : :py:class:`dict`
      Dictionary containing both input data (X_data key) and output labels (y_data key).
    n_classes : :py:class:`int`
      Number of output classes. Must be used when classification datasets are used.
    
    Returns
    -------
    prop : :py:class:`dict`
      Input/output shape and size dimensions.
    """
    # Get input and output datasets
    X_data, y_data = next(iter(data))
    # Extract input/output size and shapes
    prop = {}
    prop['input_shape'] = X_data.shape[1:]
    prop['input_size'] = numpy.prod(prop['input_shape'])
    prop['output_shape'] = y_data.shape[1:] if n_classes==None else torch.Size([n_classes])
    prop['output_size'] = numpy.prod(prop['output_shape'])
    return prop

def get_fct(category,fct=None):
    """
    Load PyTorch function of target element.
    
    Parameters
    ----------
    category : :py:class:`str`
      Target type of function to lookup in PyTorch (i.e. activation, loss, or optimizer function).
    fct : :py:class:`str`
      Target function to lookup with the above category.
    """
    pytorch_dict = {
        # Activation functions,
        'activation':{
            'elu': torch.nn.ELU,
            'exponential': None,
            'hard_sigmoid': torch.nn.Hardsigmoid,
            'linear': torch.nn.Linear,
            'relu': torch.nn.ReLU,
            'selu': torch.nn.SELU,
            'sigmoid': torch.nn.Sigmoid,
            'softmax': torch.nn.Softmax,
            'softplus': torch.nn.Softplus,
            'softsign': torch.nn.Softsign,
            'tanh': torch.nn.Tanh,
        },
        # Loss functions
        'loss':{
            'binary_crossentropy': torch.nn.BCELoss,
            'categorical_crossentropy': torch.nn.CrossEntropyLoss,
            'categorical_hinge': None,
            'cosine_proximity': None,
            'hinge': None,
            'kullback_leibler_divergence': torch.nn.KLDivLoss,
            'logcosh': None,
            'mean_absolute_error': torch.nn.L1Loss,
            'mean_absolute_percentage_error': None, 
            'mean_squared_error': torch.nn.MSELoss,
            'mean_squared_logarithmic_error': None,
            'poisson': None,
            'squared_hinge': None, 
        },
        # Optimizer functions
        'optimizer':{
            'Adadelta': torch.optim.Adadelta,
            'Adagrad': torch.optim.Adagrad,
            'Adam': torch.optim.Adam,
            'Adamax': torch.optim.Adamax,
            'Nadam': None,
            'RMSprop': torch.optim.RMSprop,
            'sgd': torch.optim.SGD,
        }
    }
    return pytorch_dict[category] if fct==None else pytorch_dict[category][fct]

def run_uq(output, log_dir, data, models, hyperprms, loss, dl_type, trial, **kwargs):
    """
    Execute Monte-Carlo Dropout Algorithm. This function loads the trained model
    architecture and does uncertainty quantification using MC dropout technique.
    
    Parameters
    ----------
    output : :py:class:`str`
      Path to model output directory where trained models are saved. This has a unique
      name that contains the value of each hyperparameter.
    log_dir : :py:class:`str`
      Path to parent repository where all output directories are stored.
    data : :py:class:`dict`
      Loaded training, validation and test datasets.
    uq : :py:class:`dict`
      Uncertainty quantification parameter settings. This corresponds to the
      UQ information provided by the user in the configuration file (
      :ref:`see here <uq>` for more details).
    """
    device = torch.device('cpu')
    # Architecture initialization
    module = importlib.import_module('.' + dl_type.lower(), 'hyppo.dnnmodels.pytorch')
    net = module.get_model(data=data['train'], prms=hyperprms, **kwargs).to(device)
    trained_models = []
    for i,model in enumerate(models):
        if type(model)==numpy.str_:
            trained_models.append(load_model(model,net,device))
        else:
            trained_models.append(model)
    dropout_rate = hyperprms.get('dropout',0.05)[0]
    if dropout_rate == 0:
        logging.warning('Running uncertainty quantification with dropout rate 0 is not optimal.')
        logging.warning('Dropout rate set to 5% for Monte Carlo dropout UQ analysis as a default.')
    pred_mean, total_var, confidence_interval = uq_quantifier(output, log_dir, data, trained_models, **kwargs)
    logging.info('-'*40)
    logging.info('OUTER OBJECTIVE FUNCTION {:>8} TRIALS'.format(len(loss)))
    logging.info('-'*40)
    logging.info('\tOuter Loss           : {:>9.5f}'.format(confidence_interval[0]))
    logging.info('\tLower Bound of CI    : {:>9.5f}'.format(confidence_interval[1]))
    logging.info('\tUpper Bound of CI    : {:>9.5f}'.format(confidence_interval[2]))
    return confidence_interval[0] #{'pred_mean':pred_mean, 'pred_var': total_var,'confidence_int':confidence_interval}
  
def load_model(fname,model,device='cpu'):
    """
    Load saved model's parameter dictionary to initialized model.
    The function will remove any ``.module`` string from parameter's name.

    Parameters
    ----------
    fname : :py:class:`str`
      Path to saved model
    model : :py:class:`torch.nn.Module`
      Initialized network network architecture
    device : :py:class:`str`
      Type of processor used (CPU or GPU'

    Returns
    -------
    model : :py:class:`torch.nn.Module`
      Up-to-date neural network model
    """
    state_dict = torch.load(fname, map_location=device)
    new_state_dict = OrderedDict()
    for key, value in state_dict.items():
        if key.startswith('module.'):
            key = key[7:]
        new_state_dict[key] = value
    model.load_state_dict(new_state_dict)
    return model

def uq_quantifier(output, log_dir, data, trained_models, criterion, uq_weights=[0.5,0.5],
                  dropout_masks=30, data_noise=0, data_type=None, update=False, device=None, **kwargs):
    data_variance = data_noise
    weights = uq_weights
    T = len(trained_models)
    alt_models=[]
    if data_variance == 0.0:
        for i in range(T):
            alt_models.append(Dropout_Model_Builder(trained_models[i]))
            # fake_model = trained_models[i]
            # alt_models.append(fake_model)
    else:
        for i in range(T):
            alt_models.append(ADF_Dropout_Model_Builder(trained_models[i],data_variance))
    uq_means = {'trained':{}, 'Unc':{}}
    uq_vars  = {'trained':{}, 'Unc':{}}
    uq_obj_vals = []
    N = dropout_masks
    logging.info('-'*40)
    logging.info('UNCERTAINTY QUANTIFICATION {:>6} MODELS'.format(T))
    logging.info('-'*40)
    logging.info('Model | Obj. Value | Dropout Mask Time')
    for j in range(T):
        if data_variance > 0.0:
            model = ADF_Dropout_Model_Builder(trained_models[j],data_variance,True)
        else:
            model = trained_models[j]
            model.eval()
        trained_val, trained_pred, trained_var, y_real = pred_evaluate(data['test'], model, criterion,update,device,**kwargs)
        uq_obj_vals.append(trained_val)
        uq_means['trained'][j] = numpy.asarray(trained_pred)
        uq_vars['trained'][j]  = numpy.asarray(trained_var)
        start_time = time.time()
        model = alt_models[j]
        model.train()
        for t in range(N): 
            val, pred, pred_var, y_real= pred_evaluate(data['test'], model, criterion, update, device, **kwargs)
            uq_obj_vals.append(val)
            uq_means['Unc'][j*N+t] = numpy.asarray(pred)
            uq_vars['Unc'][j*N+t] = numpy.asarray(pred_var)
        logging.info('{:>5} | {:>10.5f} | {:>17.3f} s'.format(j+1,trained_val.detach(),time.time()-start_time))
    pred_mean = (weights[0]/T)*sum(uq_means['trained'].values())+weights[1]*sum(uq_means['Unc'].values())/(T*N)
    data_var  = (weights[0]/T)*sum(uq_vars['trained'].values())+weights[1]*sum(uq_vars['Unc'].values())/(T*N)
    model_trained_var = torch.square(torch.tensor(uq_means['trained'][0]) - torch.tensor(pred_mean)) 
    model_Unc_var     = torch.square(torch.tensor(uq_means['Unc'][0]) - torch.tensor(pred_mean)) 
    for i  in range(1,T):
        model_trained_var = model_trained_var + torch.square(torch.tensor(uq_means['trained'][i]) - torch.tensor(pred_mean))
    for j in range(1,T*N):
        model_Unc_var = model_Unc_var + torch.square(torch.tensor(uq_means['Unc'][j]) - torch.tensor(pred_mean)) 
    model_var = (weights[0]/T)*numpy.asarray(model_trained_var)+ (weights[1]/(N*T))*numpy.asarray(model_Unc_var)
    total_var = data_var + model_var
    pred_mean_obj_val = criterion(torch.tensor(pred_mean),y_real)
    pred_std = numpy.std(torch.stack(uq_obj_vals).cpu().detach().numpy())
    if data_type=='im':
        path = os.path.join(log_dir,'output',output)
        os.makedirs(path,exist_ok=True)
        numpy.savetxt(os.path.join(path,'mean.txt'),pred_mean,fmt='%f')
        numpy.savetxt(os.path.join(path,'var.txt'),model_var,fmt='%f')
        numpy.savetxt(os.path.join(path,'y_real.txt'),y_real,fmt='%i')
    elif data_type=='ts':
        path = os.path.join(log_dir,'output',output)
        os.makedirs(path,exist_ok=True)
        trained_means = numpy.array([uq_means['trained'][key].squeeze() for key in uq_means['trained'].keys()]).T
        uq_means = numpy.array([uq_means['Unc'][key].squeeze() for key in uq_means['Unc'].keys()]).T
        numpy.savetxt(os.path.join(path,'trained_means.txt'),trained_means,fmt='%f')
        numpy.savetxt(os.path.join(path,'uq_means.txt'),uq_means,fmt='%f')
        numpy.savetxt(os.path.join(path,'pred_mean.txt'),pred_mean.squeeze(),fmt='%f')
        numpy.savetxt(os.path.join(path,'pred_var.txt'),total_var.squeeze(),fmt='%f')

    #print('uq_obj_val={}'.format(numpy.asarray(uq_obj_vals)))
    #print('pred_mean_obj_val  ={}'.format(pred_mean_obj_val))
    #print('confidence intevals = [{},{},{}]'.format(pred_mean_obj_val-2*pred_std, pred_mean_obj_val, pred_mean_obj_val+2*pred_std))
    #print('pred_mean = {}'.format(pred_mean.squeeze()))
    #print('total var = {}'.format(total_var.squeeze()))
    #print('number correct:{}'.format(numpy.count_nonzero((numpy.asarray(y_real)-numpy.argmax(numpy.asarray(uq_means['trained'][0]),axis=1))==0)))
    #print('trained model pred={}'.format(numpy.argmax(numpy.asarray(uq_means['trained'][0]),axis=1)))

    # Return statistics
    lb = pred_mean_obj_val-2*pred_std
    ub = pred_mean_obj_val+2*pred_std
    confidence_interval = [pred_mean_obj_val,lb,ub]
    
    return pred_mean, total_var, confidence_interval

############################################################################################
# These classes construct the layers which propogate data uncertianty using ADF
#-------------------------------------------------------------------------------------------
class ADF_Linear_Layer(torch.nn.Module):
    def __init__(self,Linear):
        super(ADF_Linear_Layer, self).__init__()
        self.W = Linear.weight.detach()
        self.b = Linear.bias.detach()        
    def forward(self, X):
        term_1 = torch.matmul(self.W,X[0,:].T.float()).T
        term_2 = torch.reshape(self.b,term_1.size())
        X_out = torch.zeros((2,term_1.size(0)))
        X_out[0,:] = term_1 + term_2
        X_out[1,:] = torch.matmul((self.W*self.W),X[1,:].T.float()).T
        return X_out
    
class ADF_Dropout_Layer(torch.nn.Module):
    def __init__(self,dropout_rate):
        super(ADF_Dropout_Layer, self).__init__()
        self.p = dropout_rate     
    def forward(self, X):
        X_out = torch.zeros(X.size())
        drop_vec = torch.tensor(numpy.random.binomial(1,1-self.p,X.size(1)))
        X_out[0,:] = drop_vec*X[0,:]*(1/(1-self.p))
        X_out[1,:] = drop_vec*X[1,:]*(1/(1-self.p))
        return X_out
    
class ADF_ReLU_Layer(torch.nn.Module):
    def __init__(self):
        super(ADF_ReLU_Layer,self).__init__()
    def forward(self,X):
        X_out = torch.zeros(X.size())
        x = X[0,:]
        y = X[1,:]
        sigma   = torch.sqrt(torch.abs(y))
        sigma[torch.where(torch.abs(sigma)<1e-10)]=0.0 # deals with numerical round-off
        ratio   = x/sigma
        x_new = x*norm.cdf(ratio) + sigma*norm.pdf(ratio)
        y_new = (x**2 + y)*norm.cdf(ratio) + x*sigma*norm.pdf(ratio) - x_new**2
        y_new[torch.where(y_new<.0)]=0.0 # deals with numerical round-off
        X_out[0,:] = x_new
        X_out[1,:] = y_new
        return X_out
    
class ADF_Other_Act_Layer(torch.nn.Module):
    def __init__(self,layer_name):
        super(ADF_Other_Act_Layer,self).__init__()
        self.name = layer_name
    def forward(self,X):
        torch_act={'Softmax': torch.nn.Softmax,'Tanh': torch.nn.Tanh,'ELU': torch.nn.ELU,'SELU': torch.nn.SELU,\
            'Softplus': torch.nn.Softplus,'Softsign': torch.nn.Softsign,'Sigmoid': torch.nn.Sigmoid,'Hardsigmoid': torch.nn.Hardsigmoid}
        X_out = torch.zeros(X.size())
        in_mean = X[0,:]
        in_std = torch.sqrt(X[1,:])
        if self.name in torch_act:
            f = lambda x,mean,std: torch_act[self.name]()(torch.tensor(x))*norm.pdf((x-mean)/std)/std
            g = lambda x,mean,std: (torch_act[self.name]()(torch.tensor(x))**2)*norm.pdf((x-mean)/std)/std
        out_mean=[]
        out_var =[]
        for i in range(X.size(1)):
            out_1,err_1 = quad(f, -numpy.inf, numpy.inf, args=(in_mean[i],in_std[i]), limit=150, epsabs=1e-6)
            out_2,err_2 = quad(g, -numpy.inf, numpy.inf, args=(in_mean[i],in_std[i]), limit=150, epsabs=1e-6)
            out_var.append(-out_1**2 + out_2)
            out_mean.append(out_1)
        out_mean = torch.tensor(out_mean)
        out_var  = torch.tensor(out_var)
        X_out[0,:] = out_mean
        X_out[1,:] = out_var
        return X_out

def adf_layer_selector(model, lay_num, lay_name, dropout_rate):
    if lay_name == 'Linear':
        layer = ADF_Linear_Layer(model.layers[lay_num])
    elif lay_name == 'Dropout':
        layer = ADF_Dropout_Layer(dropout_rate)
    elif lay_name == 'ReLU':
        layer = ADF_ReLU_Layer()
    else:
        layer = ADF_Other_Act_Layer(lay_name)
    return layer

############################################################################################
class ADF_Dropout_Model_Builder(torch.nn.Module):
    
    def __init__(self, model, data_noise, exact = False):
        super(ADF_Dropout_Model_Builder, self).__init__()
        self.in_size = model.prop['input_size']
        self.out_shape = model.prop['output_shape']
        self.noise = data_noise
        lay_names = []
        for i in range(len(model.layers)):
            lay_names.append(repr(type(model.layers[i])).split(".")[-1].split("'")[0])
        if 'Dropout' in lay_names:
            indx = lay_names.index('Dropout')
            p_drop = model.layers[indx].p
            drop_in = True
        elif exact:
            p_drop = 0.0
            drop_in = False
        else:
            p_drop = 0.05 # This the default dropout rate for the dropout masks
            drop_in = False
        layers = []
        for i in range(len(model.layers)):
            if drop_in:
                layers.append(adf_layer_selector(model, i, lay_names[i], p_drop))
            else:
                if lay_names[i] == 'Linear':
                    layers.append(adf_layer_selector(model, i, lay_names[i], p_drop))
                else:
                    layers.append(adf_layer_selector(model, i, lay_names[i], p_drop))
                    layers.append(adf_layer_selector(model, i,'Dropout', p_drop))
        self.layers = torch.nn.Sequential(*layers)
        
    def forward(self,data):
        data = data.reshape(data.shape[0],self.in_size)
        out_mean = torch.zeros(data.shape[0],*self.out_shape)
        out_var  = torch.zeros(data.shape[0],*self.out_shape)
        for i in range(data.shape[0]):
            input_data = data[i]
            X = torch.zeros((2,data.size(1)))
            X[0,:] = input_data
            X[1,:] = self.noise*torch.ones(input_data.size())
            out = self.layers(X)
            out_mean[i] = out[0,:]
            out_var[i]  = out[1,:]
        return {'mean':out_mean, 'var': out_var} 

############################################################################################
class Dropout_Model_Builder(torch.nn.Module):

    def __init__(self, model, **kwargs):
        super(Dropout_Model_Builder, self).__init__()
        self.in_size = model.prop['input_size']
        self.out_shape = model.prop['output_shape']
        lay_names = []
        for i in range(len(model.layers)):
            lay_names.append(repr(type(model.layers[i])).split(".")[-1].split("'")[0])
        self.lay_names = lay_names
        self.in_model = model
        if 'Dropout' in lay_names:
            indx = lay_names.index('Dropout')
            p_drop = model.layers[indx].p
            drop_in = True
        else:
            p_drop = 0.05 # This the default dropout rate for the dropout masks
            drop_in = False
        layers = []
        for i in range(len(model.layers)):
            if drop_in:
                if lay_names[i] == 'Dropout':
                    layers.append(torch.nn.Dropout(p = p_drop))
                else:
                    layers.append(model.layers[i])
            else:
                if lay_names[i] in ['ReLU','ELU','Hardsigmoid','SELU','Sigmoid','Softmax','Softplus','Softsign','Tanh']:
                    layers.append(model.layers[i])
                    layers.append(torch.nn.Dropout(p = p_drop))
                else:
                    layers.append(model.layers[i])
        self.layers = torch.nn.Sequential(*layers)

    def forward(self,data):
        if self.lay_names[0] == 'Linear':
            data = data.reshape(data.shape[0],self.in_size) #This will need to be update to use size and shape function
            out = self.layers(data)
            out = out.reshape(data.shape[0],*self.out_shape)
        elif self.lay_names[0] == 'Conv2d':
            out = self.layers(data)
            out = out.reshape(data.shape[0],*self.out_shape)
        elif self.lay_names[0] == 'LSTM':
            out =  self.layers(data)
        return out

def pred_evaluate(data, model, loss_function, update=False, device=None, **kwargs):
    device = torch.device('cpu')
    model = model.to(device)
    y_pred_mean = []
    y_pred_var  = []
    target, label = next(iter(data))
    target = target.to(device).float()
    label = label.to(device).float()
    if update and label.dim()>1 and label.shape[-1]==1:
        input_data = target[0].unsqueeze(0)
        y_real = data.dataset[:][1].float()
        for i in range(len(data.dataset)):
            input_data = input_data.to(device)
            out = model(input_data.float()).to(device)
            if type(out) is dict:
                y_pred_mean.extend(out['mean'])
                y_pred_var.extend(out['var'])
                input_data = torch.cat([input_data,out['mean']],dim=3)[:,:,:,1:]
            else:
                out = model(input_data.float()).to(device)
                y_pred_mean.extend(out)
                y_pred_var.extend(numpy.zeros(numpy.shape(out)))
                input_data = torch.cat([input_data,out],dim=3)[:,:,:,1:]
    else:
        y_real = []
        for target,label in data:
            target = target.to(device)
            out = model(target.float()).to(device)
            y_real.extend(label)
            if type(out) is dict:
                y_pred_mean.extend(out['mean'])
                y_pred_var.extend(out['var'])
            else:
                y_pred_mean.extend(out)
                y_pred_var.extend(numpy.zeros(numpy.shape(out)))
        y_real = torch.stack(y_real)
    y_pred_mean = torch.stack(y_pred_mean)
    loss = loss_function(y_pred_mean.to(device), y_real.to(device))
    return loss, y_pred_mean.cpu().detach().numpy(), torch.tensor(numpy.asarray(y_pred_var)), y_real

def time_series_uq_plotter(output, data, trained_means, pred_mean, pred_var, uq_means, plot_title):
    train_data   = data['train']
    valid_data   = data['valid']
    test_data    = data['test']
    y_real_train = train_data.dataset[:][1].float().detach().numpy()[:,0,0]
    y_real_valid = valid_data.dataset[:][1].float().detach().numpy()[:,0,0]
    y_real_test  = test_data.dataset[:][1].float().detach().numpy()[:,0,0]
    y_real       = numpy.concatenate((y_real_train,y_real_valid))
    test_indx    = numpy.size(y_real)
    y_real       = numpy.concatenate((y_real, y_real_test))
    x_pred       = numpy.asarray([i for i in range(test_indx,test_indx+numpy.size(y_real_test))])
    os.makedirs('plot_data/time series',exist_ok=True)
    plt.style.use('seaborn')
    plt.figure(figsize=(6,4),dpi=200)
    plt.plot(y_real,lw=0.5,zorder=1,color='grey',label='Observed')
    #for i in range(len(uq_means)):
    for i in range(3):
        plt.plot(x_pred, uq_means[i].squeeze(),lw=0.5,zorder=2,label='Trial #%i'%(i+1))
    #plt.fill_between(x_pred,
    #                 pred_mean.squeeze()-2*numpy.sqrt(pred_var.squeeze()),
    #                 pred_mean.squeeze()+2*numpy.sqrt(pred_var.squeeze()),
    #                 alpha=0.4,color='orange',zorder=3)
    #plt.fill_between(x_pred,
    #                 pred_mean.squeeze()-numpy.sqrt(pred_var.squeeze()),
    #                 pred_mean.squeeze()+numpy.sqrt(pred_var.squeeze()),
    #                 alpha=0.5,color='yellow',zorder=4)
    #for i in range(len(trained_means)):
    #    plt.plot(x_pred, trained_means[i].squeeze(),color='black',ls='dashed',lw=0.5,zorder=5)
    #plt.plot(x_pred,pred_mean.squeeze(),color='green',lw=1,zorder=6)
    plt.xlim([2800,3200])
    plt.ylim([0,1])
    plt.xlabel('Day')
    plt.ylabel('Normalized Temperature')
    plt.tight_layout()
    plt.legend(loc='best')
    plt.savefig(os.path.join('logs/output',output,'time_series',plot_title+'.pdf'))
    plt.close()
