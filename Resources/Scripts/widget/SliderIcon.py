
# coding:utf-8

from widget import Widget
from utils.suger import *

class SliderIcon(Widget):

    lock = False
    sel = 0

    def init(self):
        pic1 = flux.View()
        pic1.SetSize(6, 6).SetHUD(True)

        pic2 = flux.View()
        pic2.SetSize(6, 6).SetHUD(True).SetVisible(False)

        txt = flux.TextView('wqy', 40)
        txt.SetHUD(True)

        self.add(pic1)
        self.add(pic2)
        self.add(txt)

    def SetPosition(self, x, y):
        self['pic1'].SetPosition(x, y+2)
        self['txt'].SetPosition(x, y-2)
        self.x, self.y = x, y

    def SetData(self, data):
        self.data = data
        self['txt'].SetText(data[0][0])
        self['pic1'].SetSprite(data[0][1])


    def OnMove(self, select_index):
        pass

    def OnSelect(self, selct_index):
        pass

    def KeyInput(self, key, scancode, action, mods):
        def _update(step):
            if not self.lock and 0 <= self.sel + step < len(self.data):
                self.sel += step
                self.lock = True
                self.OnMove(self.sel)
                self['pic2'].SetSprite(self.data[self.sel][1])

                if step < 0:
                    self['pic1'].MoveTo(0.5, self.x - 30, self.y + 2).AnimDo()
                    self['pic2'].SetPosition(self.x + 30, self.x + 2).SetVisible(True)
                    self['pic2'].MoveTo(0.5, self.x     , self.y + 2).AnimDo()
                else:
                    self['pic1'].MoveTo(0.5, self.x + 30, self.y + 2).AnimDo()
                    self['pic2'].SetPosition(self.x - 30, self.x + 2).SetVisible(True)
                    self['pic2'].MoveTo(0.5, self.x     , self.y + 2).AnimDo()

                self['pic1'], self['pic2'] = self['pic2'], self['pic1']

                sleep(0.5)
                self.lock = False
                self['txt'].SetText(self.data[self.sel][0])

        if action == flux.GLFW_PRESS:
            if key == flux.GLFW_KEY_LEFT:
                stackless.tasklet(_update)(-1).run()
            elif key == flux.GLFW_KEY_RIGHT:
                stackless.tasklet(_update)(1).run()
            elif key in (flux.GLFW_KEY_SPACE, ord('Z'), flux.GLFW_KEY_ENTER):
                self.OnSelect(self.sel)
