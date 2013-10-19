
# coding:utf-8

import time
import stackless
from lib import flux
from utils import phy, time_offset
from utils.suger import *
from collections import deque
from utils.phy import PhyIndex, PhyGroup

class InputAct(object):
    MOVE        = 1
    MOVE_CANCEL = 2
    JUMP        = 3
    ATTACK      = 4

class Person(flux.View):
    ''' 这个类姑且定义为：可操作的单位 '''

    # 物理body
    body = None
    # 人物速度
    speed = 8.0

    # 提前输入允许时间
    lifetime = 0.2
    # 行动列表
    actlst = deque()
    # 行动缓冲
    delay = False

    # 状态：向何方移动
    steering_wheel = 0
    # 状态：方向
    direction = 0
    # 状态：跳跃
    isJumping = 0
    # 状态：攻击
    isAttacking = 0
    # 状态：是否触地
    @property
    def isGrounding(self):
        return not self.isJumping and len(self.touchlst_ground)

    def __init__(self, scr):
        super(Person, self).__init__()
        self.scr = scr
        self.phy = scr.phy

        self.SetSize(7, 7)

        #self.SetSprite('Resources/Images/meizi.png', 3)
        self.SetSprite('Resources/Images/out.png', 4)
        self.AddFrameAnim('站立', 0, 0)
        self.AddFrameAnim('移动', 1,1)
        self.AddFrameAnim('攻击1', 3,3)
        self.AddFrameAnim('攻击2', 3,3)
        self.SetFrame(0)

        offset = phy.cpv(0,-1)
        body = phy.cpBodyNew(1.0, phy.INFINITY)

        shape = phy.cpCircleShapeNew(body, 1.5, offset)
        phydata = flux.PhyData(PhyIndex.CHARACTER, self, shape)
        phy.cpShapeSetUserData(shape, phydata)

        offset = phy.cpv(0,0.5)
        shape2 = phy.cpBoxShapeNew4(body, 3.4, 3, offset)
        phydata2 = flux.PhyData(PhyIndex.CHARACTER_MAIN, self, shape2)
        phy.cpShapeSetUserData(shape2, phydata2)

        self.shape = shape
        self.shape2 = shape2
        self.body = body
        self.body.phydata = phydata
        self.body.phydata2 = phydata2

        self.phy.LinkView(self,  body)
        self.phy.AddShape(shape2)
        self.phy.AddSyncShape(shape)

    def SetPosition(self, x, y):
        self.phy.SetPos(self, x, y)

    def GetBody(self):
        if not self.body:
            self.body = self.phy.GetBody(self)
        return self.body

    touchlst_ground = dict()

    def CollisionBegin(self, data1, data2):
        if data2.index == PhyIndex.GROUND:
            if data1.index == PhyIndex.CHARACTER:
                self.isJumping = 0
                hashid = data2.shape.hashid_private
                if not hashid in self.touchlst_ground:
                    self.touchlst_ground[hashid] = data2
                self.ResetState()
            elif data1.index == PhyIndex.CHARACTER_MAIN:
                # 角色可以爬墙
                self.isJumping = 0

    def CollisionEnd(self, data1, data2):
        if data1.index == PhyIndex.CHARACTER and data2.index == PhyIndex.GROUND:
            hashid = data2.shape.hashid_private
            if hashid in self.touchlst_ground:
                del self.touchlst_ground[hashid]
            self.ResetState()

    def KeyInput(self, key, scancode, action, mods):
        
        if action == flux.GLFW_PRESS:
            if key == flux.GLFW_KEY_RIGHT:
                self.steering_wheel += 1
                self.AddAct(InputAct.MOVE)
            elif key == flux.GLFW_KEY_LEFT:
                self.steering_wheel -= 1
                self.AddAct(InputAct.MOVE)
            elif key == flux.GLFW_KEY_SPACE:
                self.AddAct(InputAct.JUMP)
            elif key == ord('Z'):
                print theWorld.GetFPS()
                self.AddAct(InputAct.ATTACK)
        elif action == flux.GLFW_RELEASE:
            if key == flux.GLFW_KEY_RIGHT:
                self.steering_wheel -= 1
                self.AddAct(InputAct.MOVE_CANCEL)
            elif key == flux.GLFW_KEY_LEFT:
                self.steering_wheel += 1
                self.AddAct(InputAct.MOVE_CANCEL)

    def AddAct(self, act, param=None):
        self.actlst.append([act, time.clock(), param])
        self.DoAction()

    def ResetState(self):
        self.AnimCancel()
        self.isAttacking = 0

        if self.steering_wheel > 0:
            self.direction = 1
        elif self.steering_wheel < 0:
            self.direction = 0

        if self.isGrounding:
            # 地面
            if self.steering_wheel:
                self.PlayFrame(1, '移动').Loop()
            else:
                self.PlayFrame(10, '站立').Loop()
        else:
            # 空中
            self.SetFrame(2)
        self.SetFlip(self.direction)
        self.GetBody().v.x = self.speed * self.steering_wheel

    def Jump(self):
        ''' 跳跃。不要在此函数中设置角色动画。因为人物离地时会自然改变动画。 '''
        if self.isJumping > 0:
            self.GetBody().v.y = 0
        self.GetBody().v.y += 10
        self.isJumping += 1

    test = []

    def Attack1(self):
        self.AnimCancel()
        self.PlayFrame(1, '攻击1').Loop()
        self.GetBody().v.x = 0
        self.GetBody().v.y = 0

        pos = self.GetPosition()
        if self.direction == 0:
            offset = -5
        elif self.direction == 1:
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

    def Attack2(self):
        self.AnimCancel()
        self.PlayFrame(1, '攻击2').Loop()
        self.GetBody().v.x = 0
        self.GetBody().v.y = 0

        pos = self.GetPosition()
        if self.direction == 0:
            offset = -5
        elif self.direction == 1:
            offset = 5

        for i in self.test:
            if not i.GetAlpha():
                self.test.remove(i)

        v  = flux.View()
        v.SetSize(abs(offset), 0.1)
        v.SetPosition(pos.x + offset /2, pos.y)
        v.SetColor(0,0,1)
        v.FadeOut(0.5).AnimDo()
        self.test.append(v)
        self.scr.AddView(v)

        lst = []
        for i in self.phy.SegmentQuery(phy.cpv(pos.x, pos.y), phy.cpv(pos.x+offset, pos.y), 2, 0):
            lst.append(i)
        print u'检测到 %d 个物体' % (len(lst)-1)

    def Attack3(self):
        self.AnimCancel()
        self.PlayFrame(1, '攻击1').Loop()
        self.GetBody().v.x = 0
        self.GetBody().v.y = 0

        pos = self.GetPosition()
        if self.direction == 0:
            offset = -5
        elif self.direction == 1:
            offset = 5

        for i in self.test:
            if not i.GetAlpha():
                self.test.remove(i)

        v  = flux.View()
        v.SetSize(abs(offset), 0.1)
        v.SetPosition(pos.x + offset /2, pos.y)
        v.SetColor(0,1,0)
        v.FadeOut(0.5).AnimDo()
        self.test.append(v)
        self.scr.AddView(v)

        lst = []
        for i in self.phy.SegmentQuery(phy.cpv(pos.x, pos.y), phy.cpv(pos.x+offset, pos.y), 2, 0):
            lst.append(i)
        print u'检测到 %d 个物体' % (len(lst)-1)

    def Attack4(self):
        self.AnimCancel()
        self.PlayFrame(1, '攻击1').Loop()
        self.GetBody().v.x = 0
        self.GetBody().v.y = 0

        pos = self.GetPosition()
        if self.direction == 0:
            offset = -5
        elif self.direction == 1:
            offset = 5

        for i in self.test:
            if not i.GetAlpha():
                self.test.remove(i)

        v  = flux.View()
        v.SetSize(abs(offset), 0.1)
        v.SetPosition(pos.x + offset /2, pos.y)
        v.SetColor(1,0,1)
        v.FadeOut(0.5).AnimDo()
        self.test.append(v)
        self.scr.AddView(v)

        lst = []
        for i in self.phy.SegmentQuery(phy.cpv(pos.x, pos.y), phy.cpv(pos.x+offset, pos.y), 2, 0):
            lst.append(i)
        print u'检测到 %d 个物体' % (len(lst)-1)

    def DoAction(self):
        def do():
            while self.actlst:
                # 是否在阻塞？阻塞中直接返回
                if self.delay:
                    return False

                # 是否超时？超时则丢弃
                tnow = time.clock()
                act, tact, param = self.actlst.popleft()
                if tnow - tact > self.lifetime:
                    continue

                if act == InputAct.MOVE:
                    self.ResetState()
                elif act == InputAct.MOVE_CANCEL:
                    if not self.isAttacking:
                        self.ResetState()
                elif act == InputAct.JUMP:
                    # 跳跃
                    if self.isJumping < 3 and not self.isAttacking:
                        self.Jump()
                elif act == InputAct.ATTACK:
                    if self.isGrounding:
                        # 地面
                        self.delay = True
                        if self.isAttacking == 0:
                            self.isAttacking = 1
                            self.Attack1()
                            sleep(0.3)
                            self.delay = False
                        elif self.isAttacking == 1:
                            self.isAttacking = 2
                            self.Attack2()
                            sleep(0.3)
                            self.delay = False
                            sleep(0.3)
                            if self.isAttacking == 2:
                                self.isAttacking = 3
                        # 第三下攻击
                        elif self.isAttacking == 2:
                            self.isAttacking = 4
                            self.Attack3()
                            sleep(0.3)
                            self.isAttacking = 0
                            self.ResetState()
                            self.delay = False
                        # 延时后的第三下攻击
                        elif self.isAttacking == 3:
                            self.isAttacking = 5
                            self.Attack4()
                            sleep(0.3)
                            self.delay = False
                            self.isAttacking = 0
                            self.ResetState()
                    else:
                        # 空中
                        if self.isAttacking == 0:
                            pass
                        elif self.isAttacking == 1:
                            pass
                        elif self.isAttacking == 2:
                            pass

        stackless.tasklet(do)().run()
