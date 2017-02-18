from Point3D import*
import pygame
import pygame.gfxdraw
import math
import random


#General parent class for objects in the game (subclass of sprite)
class GameObject(pygame.sprite.Sprite):
    #screen
    globeRadius = 100
    viewer_distance = 3

    def __init__(self, groups, gRadius = 100):
        pygame.sprite.Sprite.__init__(self, groups) 
        self._layer = self.z
        self.getRect()
        self.createNewSurface()

        self.globeRadius = gRadius   

    #creates new surface in case needs to be overidden
    def createNewSurface(self):
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
                                    pygame.SRCALPHA)  # make it transparent
        self.image = self.image.convert_alpha()
    
    #for the sprite class (blits only the rectangle)
    def getRect(self):  # GET REKT TRU DAT
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)

    #rotates the object
    def rotate(self, angle, dir, speed):
        #angle is the angle the char is at for the object to move correctly
        if dir == "up":
            deltaAngleX = -speed*math.sin(angle)
            deltaAngleY = -speed*math.cos(angle)
        elif dir == "down":
            deltaAngleX = speed*math.sin(angle)
            deltaAngleY = speed*math.cos(angle)

        #updates the x,y coordinate depending on how it's rotated
        self.point3D.rotateX(deltaAngleX)
        self.point3D.rotateY(deltaAngleY)
        self.x, self.y = self.point3D.project(self.screen.get_width(),
                    self.screen.get_height(), self.fov, self.viewer_distance)
        self.z = self.point3D.z
        #self.updateAngle(deltaAngleX, deltaAngleY)

    #updates the radius according to how far the object is
    #and Layer and angle
    def updateRadius(self):
        self.angle1, self.angle2= self.point3D.angle1, self.point3D.angle2
        self.z = self.point3D.z
        self._layer = self.z

        for group in self.groups:
            if isinstance(group, pygame.sprite.LayeredUpdates):
                group.change_layer(self, self._layer)

        self.tempRadius = int(self.refRadius*(self.z+1.5)/self.viewer_distance)
        self.radius = self.tempRadius

    def update(self):
        self.draw()
        self.getRect()

    def addLight(self, lightSource):
         ###Light
        self.lightPoints = []
        self.lightPoints3D = []
        if self.radius >5:
            self.findLightPoints()

    def drawLight(self):

        if self.sun.angle1==0 and self.sun.angle2==0:
            pygame.draw.circle(self.image, self.lightColor, 
                (self.image.get_width()//2, self.image.get_height()//2), self.radius)
            return
        pointsToDraw = []

        #adds the points for the border of the shadow
        smollestZ = 1
        for i in range(len(self.lightPoints3D)):
            point = self.lightPoints3D[i]
            if point.z <= smollestZ:
                 smollestZ = point.z
                 smollestLocation = i

        for i in range(len(self.lightPoints3D),0,-1):
            point = self.lightPoints3D[smollestLocation-i]
            if point.z>=0:
                pointsToDraw.append(self.lightPoints[smollestLocation-i])


        #to get rid of any rogue side points
        # pointsToDraw.pop()
        # pointsToDraw.pop(0)
        #pygame.gfxdraw.filled_polygon(self.image, pointsToDraw, (255,255,255))
        #adds the points at the border of the globe
        #find outermost points (points with smallest z)

        #find intersection first

        #refAngle = self.calculateAngle()


        for angle in range(-90, 90, 10):
            #print(self.sun.angle1)
            # if isinstance(self, Globe):
            #     curAngle = math.radians(self.sun.angle1 + angle)
            # else:
            #curAngle = refAngle + math.radians(angle)
            curAngle = math.radians(self.sun.angle1 + angle)
            width, height = self.image.get_size()
            x = self.radius*math.cos(curAngle) + width//2
            y = -self.radius*math.sin(curAngle) + height//2
            
            # if (angle == -90 and self.calculateDistance(x,y,pointsToDraw[len(pointsToDraw)-1][0], pointsToDraw[len(pointsToDraw)-1][1])> self.radius):
            #     print(x,y,pointsToDraw[len(pointsToDraw)-1][0], pointsToDraw[len(pointsToDraw)-1][1], self.radius)
            #     pointsToDraw.reverse()
            pointsToDraw.append((x,y))

        pygame.gfxdraw.filled_polygon(self.image, pointsToDraw, self.lightColor)
    #finds the point on the globe where the circumference of the points 
        #should be
    # def calculateAngle(self):
    #     if self.distance == 0:
    #         return self.sun.angle1
    #     dist = self.distance
    #     intAngle = 180 - self.sun.angle1 - self.angle1
    #     intDist = dist*math.sin(math.radians(intAngle))/math.sin(math.radians(self.sun.angle1))
    #     intDist2 = self.sun.distance - intDist
    #     sunToObjDist = ((self.x-self.sun.x)**2 + (self.y-self.sun.y)**2)**(0.5)
    #     sinX = math.sin(math.radians(180-self.sun.angle1))*intDist2/sunToObjDist
    #     print(sinX)
    #     return math.asin(sinX)

    def calculateDistance(self, x1, x2, y1, y2):
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2) 

    def findLightPoints(self):

        self.numPoints = self.radius
        
        self.fov = self.viewer_distance * self.radius
        
        interval = 360/self.numPoints

        for point in range(self.numPoints):
            newPoint3D = Point3D(0,0)
            newPoint3D.rotateX(self.sun.angle2+90)
            
            newPoint3D.rotateY(-interval*point)
            print(self.sun.angle2*math.cos(math.radians(interval*point)))
            newPoint3D.rotateZ(interval*point)
            #newPoint3D = Point3D(interval*point, self.sun.angle2 + 90)#*(2*(point/self.numPoints)-1))#has to range from -1 to 1
            self.lightPoints3D.append(newPoint3D)
            (x,y) = newPoint3D.project(self.image.get_width(), self.image.get_height(),
                                                                 self.fov, self.viewer_distance)
            self.lightPoints.append((x,y))








        
        

