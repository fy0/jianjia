
# coding:utf-8

from lib import flux
from utils.phy import PhyIndex

class Person(flux.PlatformerCharacter):
    ''' 这个类姑且定义为：可操作的单位 '''

    body = None
    speed = 8.0
    isJumping = 0
    steering_wheel = 0

    def __init__(self, scr):
        super(Person, self).__init__()
        self.scr = scr
        self.phy = scr.phy

        self.SetSize(6.5/2, 9.1/2)
        #self.SetSize(4.4, 5.28)
        #self.SetSize(6.6, 7.92)

        self.SetSprite('Resources/Images/meizi.png', 3)
        #self.AddFrameAnim('left', 0,4)
        #self.AddFrameAnim('right', 27, 22)
        #self.AddFrameAnim('jumpl', 5, 8)
        #self.AddFrameAnim('jumpr', 22, 19)
        self.SetFrame(0)

        fly = flux.View()
        fly.SetAnchor(self)
        fly.SetPosition(2.5, 2.0)
        fly.SetSize(1.0, 1.0)
        self.fly = fly
        self.scr.AddView(fly)


        a = flux.View()
        a.SetAnchor(self)
        a.SetSize(10, 7)
        #a.SetPosition(0, 0.5)
        a.SetColor(0, 0, 1, 0.2)
        self.scr.AddView(a)

        b = flux.View()
        b.SetAnchor(self)
        #b.SetPosition(0, -0.5)
        b.SetColor(1, 0, 0, 0.3)
        b.SetSize(10.1, 7.1)
        self.scr.AddView(b, 1)

        c = flux.View()
        c.SetAnchor(self)
        c.SetSize(6.5/2, 9.1/2)
        c.SetColor(0,1,0,0.6)
        self.scr.AddView(c)


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
            self.SetFrame(1)

    def ResetXSpeed(self):
        if not self.isJumping:
            self.SetFrame(0)
        if self.steering_wheel > 0:
            self.SetFlip(1)
            self.fly.AnimCancel()
            self.fly.MoveTo(0.3, -2.5, 2.0).AnimDo()
            #self.fly.SetPosition(-2.5, 2.0)
        elif self.steering_wheel < 0:
            self.SetFlip(0)
            self.fly.AnimCancel()
            self.fly.MoveTo(0.3, 2.5, 2.0).AnimDo()
            #self.fly.SetPosition(2.5, 2.0)
        self.GetBody().v.x = self.speed * self.steering_wheel

    def CollisionBegin(self, data1, data2):
        self.ResetXSpeed()
        if self.GetID() == data1.v.GetID() and not ( data2 and (1 <= data2.index <= 4)):
            self.isJumping = 0
            self.SetFrame(0)

    def CollisionEnd(self, data1, data2):
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
