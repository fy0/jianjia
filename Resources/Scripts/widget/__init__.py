
# coding:utf-8

from utils import varName

class Widget(object):
    view_lst = {}

    def __init__(self, *args):
        super(Widget, self).__init__()
        self.init(*args)

    def __getitem__(self, key):
        return self.view_lst[key][0]

    def __setitem__(self, key, value):
        self.view_lst[key] = [value, 0, None]

    def add_with_name(self, name, view, layer=0, scenename=None):
        self.view_lst[name] = (view, layer, scenename)

    def add(self, view, layer=0, scenename=None):
        self.view_lst[varName(view)] = (view, layer, scenename)

    def init(self):
        pass

    def SetPosition(self, x, y):
        pass

    def KeyInput(self, key, scancode, action, mods):
        pass
