
# coding:utf-8

from utils.suger import *
from view.person import Person

class ScreenGameCallback(PyScreenCallback):

    def OnInit(self):
        person = Person(self.scr)

        self.scr.phy.AddPlatformerCharacter(person)
        self.scr.AddView(person)

        self.scr.RegKey(flux.GLFW_KEY_ESCAPE)
        self.scr.RegKey(flux.GLFW_KEY_LEFT)
        self.scr.RegKey(flux.GLFW_KEY_RIGHT)
        self.scr.RegKey(flux.GLFW_KEY_UP)
        self.scr.RegKey(flux.GLFW_KEY_DOWN)
        self.scr.RegKey(flux.GLFW_KEY_SPACE)
        self.scr.RegKey(flux.GLFW_KEY_ENTER)
        self.scr.RegKey(ord('Z'))

    def OnPush(self):
        self.scr.map.Load('Resources/Maps/level1.tmx')
        self.scr.phy.LoadTmx(self.scr.map)
        theCamera.SetFocus(self.scr['person'])

        size = self.scr.map.GetSize()
        theCamera.SetSize(size.x, size.y)

    def OnPushEnd(self):
        pass

    def OnPop(self):
        pass

    def OnResume(self, _from, code):
        pass

    def KeyInput(self, key, scancode, action, mods):
        self.scr['person'].KeyInput(key, scancode, action, mods)

class PhysicsCallback(PyChipmunkCallback):
    def CollisionBegin(self, data1, data2):
        self.scr['person'].CollisionBegin(data1, data2)
        
    def CollisionEnd(self, data1, data2):
        self.scr['person'].CollisionEnd(data1, data2)


class ScreenGame(Screen):
    def __init__(self):
        super(ScreenGame, self).__init__()
        self.cb = ScreenGameCallback(self)
        self.SetPyCallBack(self.cb)

        # tmx 地图
        self.map = flux.TmxMap()
        self.map.SetBlockSize(2.5)
        self.SetTmxmap(self.map)

        # 物理及其回调
        self.phy = flux.ChipmunkWorld()
        self.phy.SetGravity(0, -20)
        self.phy.SetScreen(self)
        theWorld.SetPhy(self.phy)

        self.phycb = PhysicsCallback(self)
        self.phy.SetPyCallBack(self.phycb)


        '''
            elif key == flux.GLFW_KEY_ESCAPE:
                #MsgBox:Show("是否想要回到标题页面？", MsgBox.STYLE_YESNO, function(index)
                #if index == MsgBox.ON_YES then
                #    theWorld:PushScreen(ScreenStart.scr)
                #end
                pass
        '''
