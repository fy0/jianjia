
# coding:utf-8

from utils.suger import *
from widget.SliderIcon import SliderIcon
from widget.IconBar import IconBar
from screen.screen_game import ScreenGame

class ScreenStartCallback(PyScreenCallback):

    def OnInit(self):
        theSound.LoadSound(101, "Resources/Sounds/se001.ogg")
        theSound.LoadSound(102, "Resources/Sounds/se002.ogg")

        size = theWorld.GetSize()

        title = flux.TextView('wqy', 35)
        title.SetPosition(0, 6).SetHUD(True)
        title.SetTextColor(1, 0.3, 0)
        title.SetText('这是个|#000000 |@40标题')

        bg = flux.View()
        bg.SetHUD(True).SetSize(size.x, size.y*3).SetPosition(0, -size.y*1)
        bg.SetSpriteFrame("Resources/Images/start/bg/sun.png", 0)

        txt = flux.TextView('wqy', 15)
        txt.SetPosition(0, -5).SetHUD(True)
        txt.SetTextColor(0,0,0)
        txt.SetText('按|#ff0000←→|#000000切换菜单项，Space或Enter开始')

        icon = SliderIcon()
        icon.SetPosition(0, 0)
        icon.SetData([
            ['开始', 'Resources/Images/start/start.png'],
            ['关于', 'Resources/Images/start/about.png'],
            ['离开', 'Resources/Images/start/quit.png']
        ])

        bottombar = IconBar(3)
        bottombar.SetPosition(0, -3.5)
        bottombar.SetData(['Resources/Images/start/start.png', 'Resources/Images/start/about.png', 'Resources/Images/start/quit.png'])

        def icon_OnMove(select_index):
            theSound.PlaySound(101)
            bottombar.SetSelect(select_index)

        def icon_OnSelect(select_index):
            theSound.PlaySound(102)
            if select_index == 0:
                theWorld.PushScreen(ScreenGame.new())
            elif select_index == 1:
                pass
            elif select_index == 2:
                theWorld.EndGame()

        icon.OnMove = icon_OnMove
        icon.OnSelect = icon_OnSelect

        self.scr.AddView(title)
        self.scr.AddView(bg)
        self.scr.AddView(txt)
        self.scr.AddView(icon)

        self.scr.RegKey(flux.GLFW_KEY_ESCAPE)
        self.scr.RegKey(flux.GLFW_KEY_LEFT)
        self.scr.RegKey(flux.GLFW_KEY_RIGHT)
        self.scr.RegKey(flux.GLFW_KEY_UP)
        self.scr.RegKey(flux.GLFW_KEY_DOWN)
        self.scr.RegKey(flux.GLFW_KEY_SPACE)
        self.scr.RegKey(flux.GLFW_KEY_ENTER)
        self.scr.RegKey(ord('Z'))

    def OnPush(self):
        pass

    def OnPushEnd(self):
        pass

    def OnPop(self):
        pass

    def OnResume(self, _from, code):
        pass

    def KeyInput(self, key, scancode, action, mods):
        self.scr['icon'].KeyInput(key, scancode, action, mods)

class ScreenStart(Screen):
    def __init__(self):
        super(ScreenStart, self).__init__()
        self.cb = ScreenStartCallback(self)
        self.SetPyCallBack(self.cb)

