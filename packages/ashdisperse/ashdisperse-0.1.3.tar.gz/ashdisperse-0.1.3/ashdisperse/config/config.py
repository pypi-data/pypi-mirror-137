import os
import numba as nb
import numpy as np
import warnings

def get_threading_layer():

    return nb.config.THREADING_LAYER

def set_threading_layer(thread_layer='omp'):

    thread_layers = ['tbb', 'omp', 'workqueue']

    if thread_layer not in thread_layers:
        raise ValueError('Invalid thread layer. Expected one of: %s' % thread_layers)

    nb.config.THREADING_LAYER = thread_layer
    return

def get_max_threads():
    return os.cpu_count()

def get_num_threads():
    return nb.get_num_threads()

def set_num_threads(n):
    max_threads = get_max_threads()
    if n>max_threads:
        warnings.warn('Request more threads than available. Setting to maximum recommended.', UserWarning)
        nb.set_num_threads(max_threads-1)
    elif n==max_threads:
        warnings.warn('Setting number of threads equal to the maximum number of threads incurs a performance penalty.', UserWarning)
        nb.set_num_threads(n)
    else:
        nb.set_num_threads(n)
    
    try:
        np.mkl.np.mkl.set_num_threads_local(1)
    except:
        pass
    return

def set_default_threads():
    max_threads = get_max_threads()
    set_num_threads(max_threads-1)
    return