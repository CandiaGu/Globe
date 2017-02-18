from Point3D import*
from GameObject import*
from GlobeObject import*
import pygame
import pygame.gfxdraw
import math
import random

class Plant(GlobeObject):
    def __init__(self, groups):
        super(Plant, self).__init__(groups)

    def grow(self):
        pass


class Tree(Plant):
    def __init__(self, charAngle, globeRadius,screen, sun, groups):
        self.groups = groups
        self.sun = sun

        self.treeHeight = 10
        self.distance = globeRadius+self.treeHeight
        self.radius, self.refRadius, self.tempRadius = 20, 20, 20#radius for drawing the frame,
                                                                    #radius for changing the radius of the object
                                                                    #radius for drawing the radius

        self.angle1, self.angle2= charAngle, 90
        self.fov = self.viewer_distance * self.distance
        self.screen = screen
        self.point3D = Point3D(self.angle1, self.angle2)
        self.x, self.y = self.point3D.project(self.screen.get_width(), 
                    self.screen.get_height(), self.fov, self.viewer_distance)
        self.z = self.point3D.z
        self.lightColor = (255,230,91)
        

        super(Tree, self).__init__( groups)
        self.addLight(sun)

    def draw(self):

        self.createNewSurface()
        self.updateRadius()
        #self.decreaseRadius()
        self.radius = self.tempRadius
        self.drawTrunk()
        
        pygame.gfxdraw.filled_circle(self.image, self.radius, self.radius, int(self.tempRadius), (130,242,158))
        self.drawTrunk()
        self.drawLight()

    def drawTrunk(self):
        self.trunkDist = self.globeRadius-20
        self.trunkfov = self.viewer_distance * self.trunkDist
        self.trunkX, self.trunkY = self.point3D.project(self.screen.get_width(), 
                    self.screen.get_height(), self.trunkfov, self.viewer_distance)


        pygame.draw.line(self.screen, (244,158, 66), (self.x, self.y), (self.trunkX, self.trunkY), 3)

    def decreaseRadius(self):
        self.refRadius -= 0.1        

    def rotate(self, angle, dir, speed):
        self.fov = self.viewer_distance * self.radius
        Globe.rotate(self, angle, dir, speed)

        self.fov = self.viewer_distance * self.distance
        super(Tree, self).rotate(angle, dir, speed)

