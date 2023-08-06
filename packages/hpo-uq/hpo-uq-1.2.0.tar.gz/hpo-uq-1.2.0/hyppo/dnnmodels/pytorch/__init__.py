# System
import os
import logging
import time
import importlib

# External
import numpy
import torch
import matplotlib.pyplot as plt
from torch.nn.parallel import DistributedDataParallel
    
def train(itrial     = 0,
          data       = None,
          hyperprms  = None,
          dl_type    = None,
          output     = None,
          debug      = False,
          trial      = 1,
          validate   = True,
          accuracy   = False,
          device     = None,
          device_ids = None,
          log_dir    = 'logs',
          split      = 'data',
          rank       = 0,
          transform  = None,
          **kwargs):
    """
    PyTorch training method. This will train built-in models available from HYPPO.
    The built-in model of your choice can be specified using the `dl_type` variable.
    
    Parameters
    ----------
    itrial : :py:class:`int`
      Index of current trial.
    data : :py:class:`dict`
      Input data sets.
    hyperprms : :py:class:`dict`
      Input set of hyperparameter values.
    dl_type : :py:class:`str`
      Type of deep learning architecture to use.
    output : :py:class:`str`
      Output directory name to save results.
    debug : :py:class:`bool`
      Flag to estimate full training processing time.
    trial : :py:class:`int`
      Number of independent trials to run.
    validate : :py:class:`bool`
      Use validation dataset to evaluate the model at the end of each epoch.
    accuracy : :py:class:`bool`
      Whether to calculate estimate, e.g., for classification.
    device : :class:`torch.device`
      Processor type to be used (CPU or GPU)
    device_ids : :py:class:`list`
      Rank of current processor used (used for data splitting)
    log_dir : :py:class:`str`
      Relative path where log files are stored
    split : :py:class:`str`
      What will be split across available resources
    rank : :py:class:`int`
      Current processor rank

    Returns
    -------
    The following outputs are stored and returned in the form of a dictionary:

    loss : :py:class:`float`
      Final training loss 
    models : :py:class:`str`
      Path to saved trained model
    data : :py:class:`dict`
      Input data
    criterion : :class:`torch.nn.modules.loss`
      Loss function used for training
    hyperprms : :py:class:`dict`
      Dictionary of hyperparameter values
      
    Examples
    --------
    """
    # Architecture initialization
    module = importlib.import_module('.' + dl_type.lower(), 'hyppo.dnnmodels.pytorch')
    model = module.get_model(data=data['train'], prms=hyperprms, **kwargs).to(device)
    model(torch.ones(1,*data['train'].dataset[0][0].shape).to(device))
    #for p in model.parameters():
    #    if p.requires_grad:
    #         print(p.name, p.data)
    logging.info('-'*40)
    logging.info('Number of parameters : {:,d}'.format(sum(p.numel() for p in model.parameters())))
    logging.info('-'*40)
    if len(device_ids)>0 and split=='data':
        model(torch.ones(1,*data['train'].dataset[0][0].shape).to(device))
        model = DistributedDataParallel(model, device_ids=device_ids)
    # Check if debugging mode (summary display) requested
    if debug==1:
        from torchsummary import summary
        print(summary(model,data['train'].dataset[0][0].shape))
        quit()
    # Initialize loss function and optimizer
    criterion = hyperprms['loss'](**hyperprms['loss_args'])
    optimizer = hyperprms['optimizer'](model.parameters(),**hyperprms['opt_args'])
    # Train single trial
    t0 = time.time()
    for epoch in range(1 if debug==2 else hyperprms['epochs']):
        logging.info('-'*40)
        logging.info('{} {:>3} / {:<3} {:>14} {:>3} / {:<3}'.format('TRIAL',itrial+1,trial,'EPOCH',epoch+1,hyperprms['epochs']))
        logging.info('-'*40)
        model.train()
        # Perform training
        start_time = time.time()
        train_loss, train_acc = 0, 0
        logging.info('\tTRAINING')
        logging.info('\t\tSize : {:>11}'.format(len(data['train'].sampler)))
        for i,(target,label) in enumerate(data['train']):
            target = target.float().to(device)
            label = label.float().to(device)
            if type(criterion).__name__=='CrossEntropyLoss':
                label = label.long()
            optimizer.zero_grad()
            out = model(target)
            loss = criterion(out, label)
            train_loss += loss.item()
            loss.backward()
            optimizer.step()
            if accuracy:
                n_correct = get_accuracy(out,label)
                train_acc += n_correct
        train_loss /= (i+1)
        logging.info('\t\tLoss : {:>11.5f}'.format(train_loss))
        if accuracy:
            train_acc /= len(data['train'].sampler)
            logging.info('\t\tAcc. : {:>11.5f} %'.format(100*train_acc))
        # logging.info('\t\tsumw : {:>11.5f}'.format(sum(p.sum() for p in model.parameters())))
        logging.info('\t\tTime : {:>11.5f} s'.format(time.time()-start_time))
        model.eval()
        if validate:
            logging.info('\tVALIDATION')
            valid_loss = evaluate(device, data['valid'], model, criterion, accuracy, **kwargs)
    # Evaluate trained model with test dataset
    logging.info('-'*40)
    logging.info('{} {:>3} / {:<3} {:>24}'.format('TRIAL',itrial+1,trial,'TESTING'))
    logging.info('-'*40)
    test_loss = evaluate(device, data['test'], model, criterion, accuracy, log_dir, output, **kwargs)
    # Save model if requested
    checkpoint_dir = os.path.join(log_dir,'checkpoints',output[:-3])
    state_path = os.path.join(checkpoint_dir,'%s.pth.tar' % os.path.basename(output))
    if split=='trial' or (split=='data' and rank==0):
        os.makedirs(checkpoint_dir, exist_ok=True)
        torch.save(model.state_dict(),state_path)
    state_path = model
    return {
        'loss':test_loss.item(),
        'loss_tf':test_loss.item() if transform==None else eval(transform).item(),
        'models':state_path,
        'data':data,
        'criterion':criterion,
        'hyperprms':hyperprms,
    }

def evaluate(device, data, model, criterion, accuracy=False, log_dir=None, output=None, update=False, **kwargs):
    model.eval()
    start_time = time.time()
    logging.info('\t\tSize : {:>11}'.format(len(data.sampler)))
    y_pred, acc = [], 0
    target, label = next(iter(data))
    target = target.float().to(device)
    label = label.float().to(device)
    if update and label.dim()>1 and label.shape[-1]==1:
        input_data = target[0].unsqueeze(0)
        y_real = data.dataset[:][1].float()
        for i in range(len(data.dataset)):
            out = model(input_data.float())
            y_pred.extend(out)
            input_data = torch.cat([input_data,out],dim=3)[:,:,:,1:]
    else:
        y_real = []
        for target,label in data:
            target = target.float().to(device)
            label = label.float().to(device)
            if type(criterion).__name__=='CrossEntropyLoss':
                label = label.long()
            out = model(target.float())
            y_real.extend(label)
            y_pred.extend(out)
            if accuracy:
                acc += get_accuracy(out,label)
        y_real = torch.tensor(y_real)
    #if log_dir!=None and output!=None:
    #    y_pred_to_save = torch.stack(y_pred).detach().numpy().squeeze()
    #    path = os.path.join(log_dir,'output',output[:-3])
    #    os.makedirs(path,exist_ok=True)
    #    plt.style.use('seaborn')
    #    plt.figure(figsize=(5,5))
    #    plt.plot(y_real.detach().numpy().squeeze(),color='blue')
    #    plt.plot(y_pred_to_save,color='orange')
    #    plt.savefig(os.path.join(path,'y_pred_%s.pdf' % output[-2:]))
    #    numpy.savetxt(os.path.join(path,'y_pred_%s.txt' % output[-2:]),y_pred_to_save,fmt='%f')
    loss = criterion(torch.stack(y_pred).to(device), y_real.to(device))
    logging.info('\t\tLoss : {:>11.5f}'.format(loss))
    if accuracy:
        logging.info('\t\tAcc. : {:>11.5f} %'.format(100*acc/len(data.sampler)))
    logging.info('\t\tTime : {:>11.5f} s'.format(time.time()-start_time))
    return loss

def get_accuracy(output,label):
    _, preds = torch.max(output, 1)
    n_correct = preds.eq(label).sum().item()
    return n_correct
