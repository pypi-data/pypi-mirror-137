from .multithreading import *
import warnings

warnings.simplefilter('always', DeprecationWarning)

warnings.warn("The 'ubcs_auxiliary.threading' class was renamed to 'ubcs_auxiliary.multithreading' to make room for 'multithreading' and 'multiprocessing'", DeprecationWarning )
