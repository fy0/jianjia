
# coding:utf-8

import locale

from lib import flux
from utils import config
from utils.suger import *
from screen.screen_start import ScreenStart
from screen.screen_game import ScreenGame

def main():
    theWorld.Init(config.TITLE, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    theWorld.LoadFont('Resources/Fonts/wqy-microhei.ttc', 'wqy')
    __world_pycb = PyWorldCallback()
    theWorld.SetPyCallBack(__world_pycb)

    a = theWorld.InitGUI('Resources/Images/DefaultSkin.png', 'Resources/Fonts/wqy-microhei.ttc')
    #print a
    #a.AddButton("aaa", flux.Vec2i(0,0), None)

    scr_start = ScreenGame()
    #scr_start = ScreenStart()
    theWorld.PushScreen(scr_start)
    #print theWorld.GetSize().x
    #print theWorld.GetSize().y
    theWorld.StartGame()

if __name__ == "__main__":
    main()
