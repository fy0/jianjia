
# coding:utf-8

import time
import inspect

def varName(var):
    lcls = inspect.stack()[2][0].f_locals
    for name in lcls:
        if id(var) == id(lcls[name]):
            return name
    return None

class _(object):
    pass

def time_offset(t):
    return time.time() - t
