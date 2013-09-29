
# coding:utf-8

''' 语法糖模块
    这一模块主要负责从引擎本身
'''
import stackless
from lib import flux
from utils import varName
from widget import Widget
from lib.flux import View, TextView

theWorld = flux.World.GetInstance()
theCamera = flux.Camera.GetInstance()
theSound = theAudio = flux.Audio.GetInstance()

sleep_channel = stackless.channel()

class PyWorldCallback(flux.PyWorldCallback):
    def OnWake(self):
        sleep_channel.send(None)

def sleep(_time):
    theWorld.SetSleep(_time)
    while sleep_channel.receive():
        break

class PyScreenCallback(flux.PyScreenCallback):
    def __init__(self, scr):
        super(PyScreenCallback, self).__init__()
        self.scr = scr

class PyChipmunkCallback(flux.PyChipmunkCallback):
    def __init__(self, scr):
        super(PyChipmunkCallback, self).__init__()
        self.scr = scr

class SceneManager(object):
    sceneobj = {'':{}}
    scenename = ''

    def __init__(self, scr):
        super(SceneManager, self).__init__()
        self.scr = scr

    def set(self, itemname, value, scenename = None):
        scenename = scenename or self.scenename
        if not scenename in self.sceneobj:
            self.sceneobj[scenename] = {}
        self.sceneobj[scenename][itemname] = value

    def get(self, itemname, scenename = None):
        scenename = scenename or self.scenename
        if scenename in self.sceneobj:
            return self.sceneobj[scenename][itemname]

    def __getitem__(self, key):
        return self.sceneobj[self.scenename][key]

    def __setitem__(self, key, value):
        self.sceneobj[self.scenename][key] = value

class Screen(flux.Screen):
    instance = None

    def __init__(self):
        super(Screen, self).__init__()
        self.sm = SceneManager(self)

    def LoadScene(self, name, x=None, y=None):
        super(Screen, self).LoadScene(name)

    def AddView(self, item, layer=0, scenename=None):
        # 对 Widget 进行处理
        if issubclass(type(item), Widget):
            for _name, v in item.view_lst.items():
                _view, _layer, _scenename = v
                super(Screen, self).AddView(_view, _layer, _scenename or '')
        else:
            super(Screen, self).AddView(item, layer, scenename or '')

        itemname = varName(item)
        self.sm.set(itemname, item, scenename)

    @classmethod
    def new(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def __getitem__(self, key):
        return self.sm[key]

    def __setitem__(self, key, value):
        self.sm[key] = value
