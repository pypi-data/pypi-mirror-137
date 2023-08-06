# Externals
import numpy
from sklearn.metrics import mean_squared_error

def mse(y_real, y_predicted):
    value = mean_squared_error(numpy.squeeze(y_real), numpy.squeeze(y_predicted))
    return value
