
# coding:utf-8

from lib import flux
from utils import phy
from utils.phy import PhyIndex, PhyGroup

class Person(flux.View):
    ''' 这个类姑且定义为：可操作的单位 '''

    body = None
    speed = 8.0
    isJumping = 0
    steering_wheel = 0

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
        for arb in self.phy.GetcpArbiterList(self.body):
            if arb.b_private.data is None:
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

    def ResetXSpeed(self):
        if not self.isJumping and self.IsOnGround():
            if self.steering_wheel == 0:
                self.AnimCancel()
                self.SetFrame(0)
            else:
                self.AnimCancel()
                self.PlayFrame(1, 'move').Loop()
            
        if self.steering_wheel > 0:
            self.SetFlip(1)
            self.fly.AnimCancel()
            self.fly.MoveTo(0.3, -2.5, 2.0).Loop()
        elif self.steering_wheel < 0:
            self.SetFlip(0)
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
                if not self.isJumping:
                    self.SetFrame(2)
        elif action == flux.GLFW_RELEASE:
            if key == flux.GLFW_KEY_RIGHT:
                self.steering_wheel -= 1
                self.ResetXSpeed()
            elif key == flux.GLFW_KEY_LEFT:
                self.steering_wheel += 1
                self.ResetXSpeed()
