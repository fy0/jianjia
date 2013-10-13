
# coding:utf-8

from lib.phy import *

class PhyIndex(object):
    CHARACTER     = -255
    GROUND        = 0
    BORDER_TOP    = 1
    BORDER_RIGHT  = 2
    BORDER_BOTTOM = 3
    BORDER_LEFT   = 4

class PhyGroup(object):
    OBJECT        = 1
    PLAYER        = 2

cpvzero = cpv(0.0, 0.0)

def cpvneg(v):
    return cpv(-v.x, -v.y)
