import logging
import functools


def monitor_results(func):
    @functools.wraps(func)
    def wrapper(*func_args, **func_kwargs):
        retval = func(*func_args, **func_kwargs)
        logging.debug('function ' + func.__name__ + '() returns ' + repr(retval))
        return retval

    return wrapper
