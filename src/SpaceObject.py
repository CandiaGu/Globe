from Point3D import*
from GameObject import*
import pygame
import pygame.gfxdraw
import math
import random

#General parent class that encompasses all objects in space
class SpaceObject(GameObject):

    def __init__(self, groups):
        super(SpaceObject,self).__init__(groups)

#Comets that fall into the earth
class Comet(SpaceObject):

    def __init__(self,screen, speed, charAngle, groups):
        self.charAngle = charAngle
        self.speed = speed
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.radius = 10 #comet radius
        self.z = 0 #height of the comet is set flat
        pos = random.choice(["top","bot","lef","rig"])#chooses where the comet spawns from
        slopeBoundaries = (10,30)
        self.setSlopeAndSpeed(pos, slopeBoundaries)
        super(Comet, self).__init__(groups)

    #sets slope and speed depending on the random position and slope boundaries
    def setSlopeAndSpeed(self, pos, sB):
        if pos == "top":
            self.x, self.y = random.randint(0,self.width), 0
            #self.slope = random.randint(sB[0],sB[1])/sB[0]
            self.speed = random.choice([-self.speed*2,-self.speed,self.speed,self.speed*2])/5
        if pos == "bot":
            self.x, self.y = random.randint(0,self.width), self.height
            #self.slope = random.randint(-sB[1],-sB[0])/sB[0]
            self.speed = random.choice([-self.speed*2,-self.speed,self.speed,self.speed*2])/5
        if pos == "lef":
            self.x, self.y = 0, random.randint(0, self.height)
            #self.slope = random.randint(-sB[1],sB[1])/sB[0]
            self.speed = random.randint(self.speed,self.speed*2)/5
        if pos == "rig":
            self.x, self.y = self.width, random.randint(0, self.height)
            #self.slope = random.randint(-sB[1],sB[1])/sB[0]
            self.speed = random.randint(-self.speed*2,-self.speed)/5

        self.slope = (self.y-300)/(self.x-300)
        # if math.asin(self.y/self.slope) == self.charAngle:
        #     self.setSlopeAndSpeed(pos,sB)

        self.ogx, self.ogy = self.x, self.y

    def draw(self):

        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, self.radius-5, (122,173,255))
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, (self.radius-5)//2, (255,255,255))
        self.drawCometTail()
        self.move()

    def drawCometTail(self):
        #for i in range(random.randint(0,4))
        pygame.draw.line(self.screen, (106,149,252), (self.ogx, self.ogy), (self.x, self.y))


    def move(self):
        self.x +=self.speed
        self.y += self.slope*(self.speed)


#contains all the background stars
class Star(SpaceObject):
    def __init__(self, globeRadius, screen, groups):
        self.groups = groups
        self.width, self.height = screen.get_size()
        #min and max size of star
        self.smol, self.big = 2,3
        self.radius = random.choice([self.smol]*5 + [self.big])
        #set star to random location in the screen
        self.x, self.y = random.randint(0, self.width), random.randint(0,self.height)
        #set random color in range
        self.color = (random.randint(200,255),random.randint(200,255),random.randint(200,255))
        #only 1/20 of stars twinkle
        self.twinkle = random.choice([True]+[False]*20)
        #increasing star size while twinkling
        self.twinkleState = True 
        #for the radius increase during twinklage
        self.tempRadius = self.radius
        #so it stays in the background
        self.z = -999
        super(Star, self).__init__(groups)

    def draw(self):
        if self.twinkle:
            self.twinkling()
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, int(self.tempRadius)-1, self.color)

    #changes the star radius to make them twinkle
    def twinkling(self):
        self.createNewSurface() #draws over current
        if self.tempRadius<self.radius:
            self.twinkleState = True
        elif self.tempRadius>=self.radius:
            self.twinkleState = False

        delta = random.choice([0.01, 0.005, 0.002])#chooses random increment to increase by
        if self.twinkleState:
            self.tempRadius += delta
        else:
            self.tempRadius -= delta

#Sun Object
class Sun(SpaceObject):

    def __init__(self, screen, groups):
        self.groups = groups
        #radius of the sun
        self.radius = 60
        #for when the perspective of the sun changes
        self.refRadius = self.radius 
        self.tempRadius = self.radius
        #distance from the the center of the globe
        self.distance = self.globeRadius+500 
        self.fov = self.viewer_distance * self.distance
        self.screen = screen
        self.point3D = Point3D(0,0)
        #gets the x,y,z and angles of the point relative to the center
        self.x, self.y = self.point3D.project(self.screen.get_width(), self.screen.get_height(),
                                                                 self.fov, self.viewer_distance)
        self.z = self.point3D.z
        self.angle1, self.angle2= self.point3D.angle1, self.point3D.angle2

        #color of the sun
        self.color = (255,240,240)
        super(Sun, self).__init__( groups)

    def draw(self):
        self.createNewSurface()
        self.updateRadius()
        for i in range(self.tempRadius-5):
            self.color = (255,240,240-2*i)
            pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, self.tempRadius - i, self.color)
        self.color = (255,240,240)

class Planet(SpaceObject):
    def __init__(self, screen, groups):
        self.groups = groups
        #radius of the sun
        self.radius = random.randint(15,50)
        #for when the perspective of the sun changes
        self.refRadius = self.radius 
        self.tempRadius = self.radius
        #distance from the the center of the globe
        self.distance = self.globeRadius+random.randint(100,500)
        self.fov = self.viewer_distance * self.distance
        self.screen = screen
        self.point3D = Point3D(random.randint(0,360),random.randint(0,180))
        #gets the x,y,z and angles of the point relative to the center
        self.x, self.y = self.point3D.project(self.screen.get_width(), self.screen.get_height(),
                                                                 self.fov, self.viewer_distance)
        self.z = self.point3D.z
        self.angle1, self.angle2= self.point3D.angle1, self.point3D.angle2

        #color of the sun
        self.color = random.choice([(255,203,17),(255,81,33),(33,140,255)])
        super(Planet, self).__init__( groups)

    def draw(self):
        self.createNewSurface()
        self.updateRadius()
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, self.tempRadius, self.color)

class Satellite(SpaceObject):
    pass

