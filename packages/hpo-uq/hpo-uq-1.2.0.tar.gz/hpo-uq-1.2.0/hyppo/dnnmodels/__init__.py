import importlib

def training(library, **kwargs):
    """
    Top-level factory function for getting your models.

    Parameters
    ----------
    library : :py:class:`str`
      Machine Learning library to be used.
    
    Returns
    -------
    train_out : :py:class:`dict`
      Output of training function.
    """
    # Import relevant module based on NN architecture and library
    library = {'pt':'pytorch','tf':'tensorflow'}[library]
    module = importlib.import_module('.' + library, 'hyppo.dnnmodels')
    return module.train(**kwargs)

def get_fct(library, **kwargs):
    """
    Top-level factory function for getting your models.
    """
    # Import relevant module based on NN architecture and library
    library = {'pt':'pytorch','tf':'tensorflow'}[library]
    module = importlib.import_module('.' + library + '.utils', 'hyppo.dnnmodels')
    return module.get_fct(**kwargs)

def run_uq(library, **kwargs):
    """
    Top-level factory function for getting your models.
    """
    # Import relevant module based on NN architecture and library
    library = {'pt':'pytorch','tf':'tensorflow'}[library]
    module = importlib.import_module('.' + library + '.utils', 'hyppo.dnnmodels')
    return module.run_uq(**kwargs)
    
