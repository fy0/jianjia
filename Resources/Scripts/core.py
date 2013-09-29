
# coding:utf-8

import locale

import stackless
from lib import flux
from utils import config
from utils.suger import *
from screen.screen_start import ScreenStart

def main():
    theWorld.Init(config.TITLE, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    theWorld.LoadFont('Resources/Fonts/wqy-microhei.ttc', 'wqy')
    __world_pycb = PyWorldCallback()
    theWorld.SetPyCallBack(__world_pycb)

    scr_start = ScreenStart()
    theWorld.PushScreen(scr_start)
    theWorld.StartGame()

if __name__ == "__main__":
    main()
