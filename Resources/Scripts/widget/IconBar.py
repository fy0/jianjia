
# coding:utf-8

from widget import Widget
from utils.suger import *

class IconBar(Widget):

    sel = 0

    def init(self, size):
        for i in range(size):
            v = flux.View()
            v.SetSize(1.25, 1.25).SetHUD(True)
            self.add_with_name(i, v)

        ptr = flux.View()
        ptr.SetHUD(True)
        ptr.SetSize(1.3, 1.3).SetColor(0.69,0.69,0.69, 0.6)

        self.size = size
        self.add(ptr)

    def SetPosition(self, x, y):
        for i in range(self.size):
            self[i].SetPosition(x + (i-1)*2, y)
        self['ptr'].SetPosition(x-2, y)
        self.x, self.y = x, y

    def SetData(self, data):
        self.data = data
        for i in range(self.size):
            self[i].SetSprite(data[i])

    def SetSelect(self, select_index):
        self.sel = select_index
        self['ptr'].SetPosition(self.x + (self.sel-1)*2, self.y)
