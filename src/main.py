"""
Based on format from
URL:     http://thepythongamebook.com/en:part2:pygame:step002
"""

####

from GameObject import* 
from SpaceObject import*
from GlobeObject import*
from Plant import*
import pygame
import pygame.gfxdraw
import math
import random
import sys
import cv2
import numpy as np
import shelve

####
class PygView(object):
    width, height = 600, 600
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)

########init
    def __init__(self, width=640, height=600, fps=40):
        pygame.init()
        pygame.display.set_caption("Press ESC to quit")
         
        self.width, self.height = width, height

        #draws the background
        self.background = pygame.Surface(PygView.screen.get_size()).convert()
        self.background.fill((10,35,75))# makes background blue
        self.drawStaticBackground()

        #updates clock
        self.clock = pygame.time.Clock()
        self.fps = fps# frames per second
        self.playtime = 0.0

        #initializes objects
        self.initObjects()

        #fonts
        self.font = pygame.font.SysFont('acaslonproregular', 25)
        self.font2 = pygame.font.SysFont('acaslonproregular', 18)

        #modes
        self.gameOver = False
        self.nextLevel = False
        self.howTo = False
        self.splash = True
        self.pause = False

        #for gameplay
        self.cometTime = 0
        self.intervalTime = 3
        self.level = 0
        self.nextLevel = False
        self.death = 0
        self.cometSpeed = 5
        self.perpetual = True


        self.input = None

    #initializes globe and objects around it
    def initObjects(self):
        self.gRadius =100
        self.gx, self.gy = self.width//2, self.height//2

        self.orderedObjects = pygame.sprite.LayeredUpdates()
        self.rotatableObjects = pygame.sprite.LayeredUpdates()

        
        self.initSpaceObjects()
        self.initGlobeObjects()
       
    def initGlobeObjects(self):
        ###Globe
        self.globe = Globe(PygView.screen, self.sun, (self.orderedObjects, self.rotatableObjects))

        ###Character
        self.char = Character(self.gx, self.gy, self.gRadius, self.orderedObjects)

        ###Trees
        self.trees = pygame.sprite.Group()

        ###Craters
        self.craters = pygame.sprite.Group()

        ###Clouds
        self.clouds = pygame.sprite.Group()

        #self.drawTest()

    def initSpaceObjects(self):
        ###Stars
        self.numStars = 500
        self.stars = pygame.sprite.Group()
        for i in range(self.numStars):
            Star(self.gRadius, PygView.screen,(self.stars,self.orderedObjects))

        ###Comets
        self.comets = pygame.sprite.Group()

        ###Space Things
        self.spaceThings = pygame.sprite.Group()
        self.sun = Sun(PygView.screen, (self.orderedObjects,self.rotatableObjects,self.spaceThings))
        for i in range(random.randint(4,8)):
            Planet(PygView.screen, (self.orderedObjects,self.rotatableObjects,self.spaceThings))


#########run
    def run(self):
        ###mainloop
        self.running = True
            #whether game is being played
        self.play = False
            #transition to next level
        self.nextLevel = False

        while self.running:
            #####testing shit
            #print(self.char.point3D.angle1)
            ####
            if not self.pause and not self.gameOver: 
                self.drawObjects(True)
                self.runPerpetual()
            else:
                self.drawObjects(False)

            if self.nextLevel and self.play:
                self.initiateNextLevel()
            self.keyQuit()
            self.checkMode()


            

            #updates the screen and draws images on top of one another
            pygame.display.flip()
            PygView.screen.blit(self.background, (0, 0))
            
        pygame.quit()

#########helper

    def initiateNextLevel(self):
        
        self.level += 1
        angle = 0
        for cloud in self.clouds:
            cloud.kill()
        for tree in self.trees:
            tree.kill()
        for crater in self.craters:
            crater.kill()
        for comet in self.comets:
            comet.kill()
        self.char.hold = False
        newComets = pygame.sprite.Group()
        for i in range(self.level):
            newComets.add(Comet(self.screen, 5, self.char.angle, (self.comets, self.orderedObjects)))
        while len(newComets) != 0:
            self.drawObjects()
            if self.level>1:
                self.nextLevelTransition()
            self.checkCollision()
            pygame.display.flip()
            PygView.screen.blit(self.background, (0, 0))

        # for i in range(self.level):
        #     while angle in randomCraterAngle:
        #         angle = random.randint(0,90)
        #     randomCraterAngle.add(angle)
        #     Crater(angle*4, self.gRadius,self.screen,
        #                  (self.orderedObjects, self.rotatableObjects, self.craters))
        self.death = 0
        self.cometSpeed +=1
        if self.intervalTime > 1:
            self.intervalTime -= 0.5
        self.nextLevel = False

    def runPerpetual(self):
        if self.perpetual:
            self.rotateObjects("up",1,90)

    def createComets(self):
        #new comet generate every second
        if self.cometTime > self.intervalTime:
            #if face detected, generates new comets
            self.detectFace()
            if not PygView.faceDetected:
                self.pause = True
            else:
                self.pause = False
                Comet(self.screen, self.cometSpeed, self.char.angle,(self.comets, self.orderedObjects))
            self.cometTime = 0


    #check if game quit

    def keyQuit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    # if not self.howTo:
                    #     self.play = True
                    #     self.initiateNextLevel()
                    if (self.gameOver and not self.howTo) or self.splash:
                        self.play = True
                        self.level = 0
                        self.cometSpeed = 5
                        self.initiateNextLevel()
                        self.gameOver = False
                        self.splash = False
                if event.key == pygame.K_h:
                    self.howTo = not(self.howTo)
                if event.key == pygame.K_p:
                    self.pause = not(self.pause)


    #checks user input(and if key held, input recorded as multiple)
    def keyPressed(self, keys):
        print(self.char.angle)
        if keys[pygame.K_LEFT]:
            self.char.move("left")

        elif keys[pygame.K_RIGHT]:
            self.char.move("right")

        elif keys[pygame.K_UP]:
            self.perpetual = False
            self.rotateObjects("up",5, self.char.angle)
            

        elif keys[pygame.K_DOWN]:
            self.perpetual = False
            self.rotateObjects("down",5, self.char.angle)
            
        elif keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            #lets go of item if touching crater
            for crater in self.craters:
                if pygame.sprite.collide_circle(self.char, crater) and self.char.hold:
                    self.char.hold = False
                    tree = Tree(self.char.angle, self.gRadius, self.screen, self.sun,(self.orderedObjects, self.rotatableObjects, self.trees))
                    crater.kill()
            if len(self.craters) == 0 :
                self.nextLevel = True
        self.perpetual = True


    #check item collisions and responds accordingly
    def checkCollision(self):
        for comet in self.comets:
            if pygame.sprite.collide_circle(self.char, comet):
                self.char.hold = True
                comet.kill()
            #kills comet when it goes off screen
            elif not (0<=comet.y<=self.height and 0<= comet.x<=self.width):
                 comet.kill()

            #creates crater if comet comes in contact with globe
            elif pygame.sprite.collide_circle(self.globe, comet):
                if self.gx - comet.x == 0:
                    comet.x += 0.01

                #finds the angle at which the comet comes in
                craterAngle = math.degrees(math.atan((self.gy-comet.y)/(self.gx-comet.x)))
                if (self.gx-comet.x>0):
                    craterAngle += 180

                self.craters.add(Crater(craterAngle, self.gRadius,self.screen,
                         (self.orderedObjects, self.rotatableObjects, self.craters)))

                comet.kill()
                self.death +=1

                for i in range(random.randint(1,3)):
                    self.orderedObjects.add(Cloud(craterAngle, self.gRadius, self.screen,self.sun, 
                        (self.orderedObjects, self.rotatableObjects, self.clouds)))


    #rotates objects when prompted
    def rotateObjects(self, dir, speed, angle):
        for obj in self.rotatableObjects:
            obj.rotate(angle, dir, speed)

    def checkMode(self):
        if self.death >= 3:
            self.gameOver = True
            self.play = False
            self.gameOverMode()
        elif self.howTo == True:
            self.howToMode()
        elif self.play:
            self.playMode()
        elif self.splash:
            self.splashMode()
        elif self.pause:
            self.pauseMode()
##modes

    def howToMode(self):
        self.keyPressed(pygame.key.get_pressed())
        self.draw_text("To move left or right, press the left or right key ",self.width//2, self.height//5, self.font2,(255,255,255))
        self.draw_text("To rotate the globe, press the up or down key ",self.width//2, self.height//5 + 30, self.font2,(255,255,255))
        self.draw_text("To play, catch comets falling from the sky",self.width//2, self.height//5 + 300, self.font2,(255,255,255))
        self.draw_text("Drop those comets into the craters on the globe to plant trees",self.width//2, self.height//5 + 330, self.font2,(255,255,255))
        self.draw_text("If comet is not caught, it creates a new crater to be filled",self.width//2, self.height//5 + 360, self.font2,(255,255,255))
        self.draw_text("Once all the craters are filled, you move on to the next level!",self.width//2, self.height//5 + 390, self.font2,(255,255,255))
        self.draw_text("You lose if you miss three comets in one round",self.width//2, self.height//5 + 420, self.font2,(255,255,255))
        self.draw_text("press h to return", self.width//2, self.height//2, self.font, (0,0,0))


    def gameOverMode(self):
        self.draw_text("game over", self.width//2, self.height//2, self.font, (0,0,0))
        self.draw_text("press space to start over", self.width//2, self.height//2 +30, self.font2, (0,0,0))

    def splashMode(self):
        self.draw_text("GLOBE", self.width//2, self.height//2, self.font,(0,0,0))
        self.draw_text("press space to begin", self.width//2, self.height//2-30, self.font2, (0,0,0))
        self.draw_text("press 'h' for tutorial", self.width//2, self.height//2+30, self.font2, (0,0,0))

    def pauseMode(self):
        self.play = False
        self.draw_text("press p to unpause", self.width//2, self.height//2, self.font,(0,0,0))

    def playMode(self):
        self.keyPressed(pygame.key.get_pressed())
        self.checkCollision() 
        self.updateTime()
        self.createComets()
        self.draw_text("Level: " + str(self.level), self.width//5*4, self.height//5*4, self.font, (255,255,255))
        self.draw_text("Deaths: " + str(self.death), self.width//5*4, self.height//5*4 + 30, self.font, (255,255,255))
        self.draw_text("Face Detected: " + str(self.faceDetected), self.width//5*4, self.height//5*4 + 60, self.font2, (255,255,255))

    def nextLevelTransition(self):
        self.draw_text("Level Up!", self.width//2, self.height//2, self.font,(0,0,0))

    #draws actual Objects
    def drawObjects(self, update = True):
        self.drawBackgroundObjects()
        
        self.orderedObjects.clear(PygView.screen, self.background)
        if update == True:
            self.orderedObjects.update()
        self.orderedObjects.draw(PygView.screen)
        self.drawText()

    def drawText(self):
        
       pass
        


    def drawBackgroundObjects(self):
        for i in range(self.numCircles):
            pygame.draw.circle(self.background, self.colors[i], self.bgPos[i], self.bgRadius[i])

        self.stars.update()
        self.stars.draw(PygView.screen)

    def drawStaticBackground(self):

        self.numCircles = 100
        self.colors = []
        for i in range(self.numCircles):
            self.colors.append((10+random.randint(-10,10),35+random.randint(-10,10),75++random.randint(-10,10)))
        self.bgPos = []
        self.bgRadius = []
        for i in range(self.numCircles):
            self.bgPos.append((random.randint(0,self.screen.get_width()),random.randint(0,self.screen.get_height())))
            self.bgRadius.append(random.randint(0,100))
        


    #from tutorial
    def draw_text(self, text, x, y, font, color):
        """Center text in window
        """
        fw, fh = font.size(text) # fw: font width,  fh: font height
        surface = font.render(text, True, color)
        # 
        self.screen.blit(surface, ((x - fw//2), (y - fh//2)))

    #updates time
    def updateTime(self):
        milliseconds = self.clock.tick(self.fps)
        self.playtime += milliseconds / 1000.0
        self.cometTime +=milliseconds / 1000.0


#####Facial Detection just cus lol
####From opencv tutorial
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)
    faceDetected = False
    def detectFace(self):

        video_capture = PygView.video_capture
        face_cascade = PygView.face_cascade
        # Capture frame-by-frame
        (ret, frame) = video_capture.read()
        
        #Flips image
        frame = cv2.flip(frame,1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(frame, 1.3, 5)

        if len(faces) == 0:
            PygView.faceDetected = False
        else:
            PygView.faceDetected = True

        #cv2.imshow('img', frame)
        k = cv2.waitKey(1) 

####

if __name__ == '__main__':

    # call with width of window and fps
    PygView(600, 600).run()
    PygView.video_capture.release()
    cv2.destroyAllWindows()

