# System
import os
import ast

# External
import numpy
import yaml
import pickle5 as pickle

# Local
from .extract import get_samples

def slurm(config,**kwargs):
    make_slurm_script(config['path'],**config['dist'])
    
def make_slurm_script(path, sbatch={}, operation='evaluation', log_dir='logs', nsteps=1, ntasks=1,
                      node_type='cpu', module=None, conda='', cd=None, export=None, 
                      proc_per_node=None, **kwargs):
    if proc_per_node==None:
        proc_per_node = 8 if node_type=='gpu' else 32
    script = open('%s.sh' % operation,'w')
    script.write('#!/bin/bash\n')
    # ----------------------------------------------
    #   SBATCH directive
    # ----------------------------------------------
    for key,value in sbatch.items():
        script.write('#SBATCH --%s %s\n'%(key,value))
    if node_type=='cpu':
        script.write('#SBATCH --nodes %i\n' % nsteps )
        script.write('#SBATCH --ntasks-per-node %i\n' % ntasks )
    if node_type=='gpu':
        script.write('#SBATCH --nodes %i\n' % numpy.ceil(nsteps * ntasks / proc_per_node) )
        script.write('#SBATCH --ntasks %i\n' % (nsteps * ntasks) )
        script.write('#SBATCH --dependency singleton\n')
        script.write('#SBATCH --exclusive\n')
    script.write('#SBATCH --%ss-per-task 1\n' % node_type)
    script.write('#SBATCH --output %x-%j.out\n')
    script.write('#SBATCH --error %x-%j.err\n')
    # ----------------------------------------------
    #   Load modules
    # ----------------------------------------------
    script.write('module load parallel\n')
    if module!=None:
        for mod in module.split(';'):
            script.write('module load %s\n' % mod)
    if conda!='':
        script.write('conda activate %s\n' % conda)
        conda = 'conda activate %s &&' % conda
    if export!=None:
        script.write('export PYTHONPATH=$PYTHONPATH:%s\n' % export)
    # ----------------------------------------------
    #   SBATCH directive
    # ----------------------------------------------
    if cd!=None:
        script.write('cd %s\n' % cd)
    script.write('mkdir -p %s\n' % log_dir)
    if operation=='evaluation':
        script.write('python $HOME/hyppo/bin/hyppo sampling config.yaml\n')
    # ----------------------------------------------
    #   Parallel SRUN command
    # ----------------------------------------------
    parallel = 'parallel --delay .2 -j %i --joblog %s/runtask.log' % (nsteps, log_dir)
    srun = 'srun --exclusive --nodes 1 --ntasks %i --%ss-per-task 1' % (ntasks, node_type)
    hpo = 'python $HOME/hyppo/bin/hyppo %s config.yaml' % operation
    script.write('%s "%s %s %s && echo step {1}" ::: {0..%i}\n' % (parallel, conda, srun, hpo, nsteps-1))
    script.close()

# def slurm_split(config,**kwargs):
#     assert 'dist' in config.keys(), 'You did not add the dist section in configuration file. Abort.'
#     # Estimate total number of CPUs
#     nproc = int(config['dist']['sbatch']['nodes'])*32
#     # Write SLURM script
#     samples = get_samples('logs',surrogate=True,mult=False)
#     times   = numpy.hstack((samples['evals'][:,-1],samples['sgate'][:,-1]))
#     times   = numpy.array([numpy.ceil(time/60) for time in times])
#     samples = numpy.vstack((samples['evals'][:,:-2],samples['sgate'][:,:-2]))
#     script  = ''
#     for i in range(len(samples)):
#         trial_path = os.path.abspath('trials/sample_%03i/'%(i+1))
#         os.makedirs(trial_path,exist_ok=True)
#         samp_to_save = numpy.array([samples[i] for n in range(nproc)])
#         filehandler = open(trial_path+'/samples.pickle', 'wb')
#         pickle.dump(samp_to_save, filehandler)
#         copy_config(config,filename=trial_path+'/config.yaml')
#         write_slurm(config,nproc,path=trial_path+'/script.sh',conf=trial_path+'/config.yaml',time=times[i])
#         script += 'sbatch %s/script.sh\n'%trial_path
#     batch = open('trials/batch.sh','w')
#     batch.write(script)
#     batch.close()
        
# def copy_config(config,filename):
#     config = ast.literal_eval(config['original'])
#     config['prms']['record'] = 'samples.pickle'
#     with open(filename, 'w') as f:
#         yaml.dump(config, f, default_flow_style=False)
