
# coding:utf-8

import time
import stackless
from lib import flux
from utils import phy, time_offset
from utils.suger import *
from utils.phy import PhyIndex, PhyGroup

class Person(flux.View):
    ''' 这个类姑且定义为：可操作的单位 '''

    body = None
    # 人物速度
    speed = 8.0
    # 是否在跳跃状态
    isJumping = 0
    # 用于标识当前人物向哪里走
    steering_wheel = 0
    _dir = 0
    # 行动缓冲
    act_delay = 0
    old_time = 0

    _task = None

    def check_delay(self):
        if time_offset(self.old_time) >= self.act_delay:
            self.old_time = time.time()
            return True

    def __init__(self, scr):
        super(Person, self).__init__()
        self.scr = scr
        self.phy = scr.phy

        #self.SetSize(6.5/2, 9.1/2)
        self.SetSize(7, 7)
        #self.SetSize(4.4, 5.28)
        #self.SetSize(6.6, 7.92)

        #self.SetSprite('Resources/Images/meizi.png', 3)
        self.SetSprite('Resources/Images/out.png', 4)
        self.AddFrameAnim('move', 1,1)
        self.AddFrameAnim('attack1', 3,3)
        self.AddFrameAnim('attack2', 3,3)
        #self.AddFrameAnim('right', 27, 22)
        #self.AddFrameAnim('jumpl', 5, 8)
        #self.AddFrameAnim('jumpr', 22, 19)
        self.SetFrame(0)

        offset = phy.cpv(0,-1)
        #moment = phy.cpMomentForCircle(1.0, 2, 2, offset)
        #body = phy.cpBodyNew(1.0, moment)
        body = phy.cpBodyNew(1.0, phy.INFINITY)
        phydata = flux.PhyData(PhyIndex.CHARACTER, self)

        shape = phy.cpCircleShapeNew(body, 1.5, offset)
        phy.cpShapeSetUserData(shape, phydata)

        self.shape = shape
        self.body = body
        self.body.phydata = phydata

        self.phy.LinkView(self,  body)
        self.phy.AddSyncShape(shape)

        fly = flux.View()
        fly.SetAnchor(self)
        fly.SetPosition(2.5, 2.0)
        fly.SetSize(1.0, 1.0)
        self.fly = fly
        self.scr.AddView(fly)

    def IsOnGround(self):
        for i in self.phy.ShapeQuery(self.shape):
            if flux.CastToPhyData(i.data) is None:
                return True

    def SetPosition(self, x, y):
        self.phy.SetPos(self, x, y)

    def GetBody(self):
        if not self.body:
            self.body = self.phy.GetBody(self)
        return self.body

    def Jump(self):
        if self.isJumping < 3:
            if self.isJumping > 0:
                self.GetBody().v.y = 0
            self.GetBody().v.y += 10
            self.isJumping += 1
            self.AnimCancel()

    test = []

    def Attack(self):
        if not self.check_delay():
            return
        self.act_delay = 0.5

        def do():
            pos = self.GetPosition()
            if self._dir == 0:
                offset = -5
            elif self._dir == 1:
                offset = 5

            for i in self.test:
                if not i.GetAlpha():
                    self.test.remove(i)

            v  = flux.View()
            v.SetSize(abs(offset), 0.1)
            v.SetPosition(pos.x + offset /2, pos.y)
            v.SetColor(1,0,0)
            v.FadeOut(0.5).AnimDo()
            self.test.append(v)
            self.scr.AddView(v)

            lst = []
            for i in self.phy.SegmentQuery(phy.cpv(pos.x, pos.y), phy.cpv(pos.x+offset, pos.y), 2, 0):
                lst.append(i)
            print u'检测到 %d 个物体' % (len(lst)-1)

            self.PlayFrame(0.5, 'attack1').AnimDo()
            sleep(0.5)
            self.ResetXSpeed()

        self._task = stackless.tasklet(do)()
        self._task.run()
    
    def ResetXSpeed(self):
        if not self.isJumping and self.IsOnGround():
            if self.steering_wheel == 0:
                self.AnimCancel()
                self.SetFrame(0)
            else:
                self.AnimCancel()
                self.PlayFrame(1, 'move').Loop()

        if self.steering_wheel > 0:
            self._dir = 1
            self.SetFlip(self._dir)
            self.fly.AnimCancel()
            self.fly.MoveTo(0.3, -2.5, 2.0).Loop()
        elif self.steering_wheel < 0:
            self._dir = 0
            self.SetFlip(self._dir)
            self.fly.AnimCancel()
            self.fly.MoveTo(0.3, 2.5, 2.0).AnimDo()
        self.GetBody().v.x = self.speed * self.steering_wheel

    def CollisionBegin(self, data1, data2):
        if self.GetID() == data1.v.GetID() and not (data2 and (1 <= data2.index <= 4)):
            self.isJumping = 0
            self.SetFrame(0)
        self.ResetXSpeed()

    def CollisionEnd(self, data1, data2):
        if self.GetID() == data1.v.GetID() and not (data2 and (1 <= data2.index <= 4)):
            self.AnimCancel()
            self.SetFrame(2)
        self.ResetXSpeed()

    def KeyInput(self, key, scancode, action, mods):
        
        if action == flux.GLFW_PRESS:
            if key == flux.GLFW_KEY_RIGHT:
                self.steering_wheel += 1
                self.ResetXSpeed()
            elif key == flux.GLFW_KEY_LEFT:
                self.steering_wheel -= 1
                self.ResetXSpeed()
            elif key == flux.GLFW_KEY_SPACE:
                self.Jump()
            elif key == ord('Z'):
                self.Attack()
        elif action == flux.GLFW_RELEASE:
            if key == flux.GLFW_KEY_RIGHT:
                self.steering_wheel -= 1
                self.ResetXSpeed()
            elif key == flux.GLFW_KEY_LEFT:
                self.steering_wheel += 1
                self.ResetXSpeed()
