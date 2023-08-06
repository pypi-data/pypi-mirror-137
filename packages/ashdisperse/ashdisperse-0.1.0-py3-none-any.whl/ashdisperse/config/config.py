import os
import numba as nb
import numpy as np
import warnings

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