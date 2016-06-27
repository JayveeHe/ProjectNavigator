__author__ = 'jayvee'
import os
import arrow


def timer(func):
    def wrapper(*args, **kwargs):
        t = arrow.utcnow()
        res = func(*args, **kwargs)
        print '[%s]cost time = %s' % (func.__name__, arrow.utcnow() - t)
        return res

    return wrapper


PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
