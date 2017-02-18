from Point3D import*
from GameObject import*
import pygame
import pygame.gfxdraw
import math
import random

#contains all the objects on the globe and the globe itself 
class GlobeObject(GameObject):

    def __init__(self, groups):
        super(GlobeObject,self).__init__(groups)

#actual globe
class Globe(GlobeObject):  

    def __init__(self, screen, sun, groups):
        self.sun = sun

        self.gwidth, self.gheight = 200,200
        self.radius = self.gwidth//2

        #for sprite layering
        self.z = 0

        self.fov = self.viewer_distance * self.globeRadius
        self.screen = screen
        (self.width,self.height) = self.screen.get_size()
        self.x, self.y = self.width/2, self.height/2
        self.angle1, self.angle2 = 0,0
        self.distance = 0

        super(Globe, self).__init__(groups)

        self.lightColor = (255,255,255)
        self.addLight(sun)#this adds the light to the globe

    #overrides parent rotate
    def rotate(self, angle, dir, speed):
        if dir == "up":
            deltaAngleX = -speed*math.sin(angle)
            deltaAngleY = -speed*math.cos(angle)
        elif dir == "down":
            deltaAngleX = speed*math.sin(angle)
            deltaAngleY = speed*math.cos(angle)

        for i in range(len(self.lightPoints3D)):
            point = self.lightPoints3D[i]
            point.rotateX(deltaAngleX)
            point.rotateY(deltaAngleY)
            x, y = point.project(self.image.get_width(),
                    self.image.get_height(), self.fov, self.viewer_distance)
            self.lightPoints[i] = (x,y)
            #super(Globe, self).rotate(angle, dir, speed)

    #draws the globe circle
    def draw(self):
        self.createNewSurface()
        pygame.draw.circle(self.image, (255,100,100), (self.gwidth//2, self.gheight//2), self.radius)
        #pygame.draw.circle(self.image, (100,100,100), (self.gwidth//2, self.gheight//2), self.radius-50)
        self.drawLight()

#draws main character
class Character(GlobeObject):

    def __init__(self, gx, gy, globeRadius, groups):
        self.radius = 15
        self.gx, self.gy = gx, gy
        self.x, self.y, self.z = gx, gy-globeRadius, 0
        self.getRect()
        self.angle = -90
        self.speed = 5

        #self.point3D = Point3D(self.angle, 0)
        self.hold = False #whether holding seed or not

        super(Character, self).__init__(groups)

    #draws circle, if holding draws a black circle in the middle
    def draw(self):
        self.createNewSurface()
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, self.radius-5, (255,255,255))
        pygame.gfxdraw.circle(self.image, self.radius, self.radius, self.radius-5, (140,140,140))
        if self.hold:
            pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, self.radius-8, (140,140,140))
        pygame.gfxdraw.filled_trigon(self.image, self.radius, self.radius+5, self.radius +5 ,self.radius - 5, self.radius -5,self.radius - 5, (255, 0, 0))


    #Facter moves only on the surface of the globe
    def move(self, dir):
        #global globeRadius
        #print(self.angle)
        if dir == "left":
            self.angle -= self.speed
        elif dir == "right":
            self.angle += self.speed
        self.x = GameObject.globeRadius*math.cos(math.radians(self.angle)) + self.gx
        self.y = GameObject.globeRadius*math.sin(math.radians(self.angle)) + self.gy

    #animates the character
    def animate(self, dir):
        pass


class Smoke(GlobeObject):
    pass

#cloud arises when crater is formed
class Cloud(GlobeObject):
    def __init__(self, charAngle, globeRadius,screen, sun, groups):
        self.groups = groups

        self.distance = globeRadius + 20
        self.radius = random.randint(10,40)
        self.refRadius,self.tempRadius = self.radius,10
        self.color = (66,134, 244)

        self.fov = self.viewer_distance * self.distance
        self.screen = screen

        #initialize the 3dPoint
        self.angle1 = charAngle + random.randint(0,20)
        self.angle2 = 90 + random.randint(0,20)
        self.point3D = Point3D(self.angle1, self.angle2)
        self.z = self.point3D.z

        self.x, self.y = self.point3D.project(self.screen.get_width(), 
                    self.screen.get_height(), self.fov, self.viewer_distance)

        self.sun = sun


        super(Cloud, self).__init__( groups)

        self.lightColor = (255,255,255)
        self.addLight(sun)

    def rotate(self, angle, dir, speed):
        angle = math.radians(angle)
        self.fov = self.viewer_distance * self.radius
        if dir == "up":
            deltaAngleX = -speed*math.sin(angle)
            deltaAngleY = -speed*math.cos(angle)
        elif dir == "down":
            deltaAngleX = speed*math.sin(angle)
            deltaAngleY = speed*math.cos(angle)

    
        for i in range(len(self.lightPoints3D)):
            point = self.lightPoints3D[i]
            point.rotateX(deltaAngleX)
            point.rotateY(deltaAngleY)
            x, y = point.project(self.image.get_width(),
                    self.image.get_height(), self.fov, self.viewer_distance)
            self.lightPoints[i] = (x,y)
        Globe.rotate(self, angle, dir, speed)

        self.fov = self.viewer_distance * self.distance
        super(Cloud, self).rotate(angle, dir, speed)
        

    def draw(self):

        #so that cloud moves by itself and changes by itself
        
        #self.fov = self.viewer_distance * self.distance
        #super(Cloud, self).rotate(0, "up", 5)
        self.createNewSurface()
        self.updateRadius()
        # self.radius = self.tempRadius
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, self.tempRadius, self.color)
        self.drawLight()
        self.rotate(90, "up", 5)


    def rain(self):
        pass
        #rain animation + reduce in size

#crater is created after the comet hits the globe
#made up of multiple points for crater like shape
class Crater(GlobeObject):

    def __init__(self, craterAngle, globeRadius,screen, groups):
        self.groups = groups
        
        self.radius, self.refRadius, tempRadius = 20,20,10
        self.distance = globeRadius-self.radius

        self.fov = self.viewer_distance * self.distance
        self.screen = screen

        self.angle1, self.angle2 = craterAngle, 90
        self.fov = self.viewer_distance * self.globeRadius
        self.point3D = Point3D(self.angle1, self.angle2)
        self.x, self.y = self.point3D.project(self.screen.get_width(),
        self.screen.get_height(), self.fov, self.viewer_distance)

        self.z = self.point3D.z
        self.color = (155,155,155)

        super(Crater, self).__init__( groups)

    def draw(self):

        self.createNewSurface()
        self.updateRadius()
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, self.tempRadius, (self.color))

    #overrides the parent class
    # def rotate(self):
    #     pass

