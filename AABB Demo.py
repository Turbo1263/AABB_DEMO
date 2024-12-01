#Mason Bledsoe 2D Collision Detection 11.22.2024
import pygame as pg
import random
import math

#EDIT ME
speed = 1

playerHeight = 20
playerWidth = 20

collectWidth = 20
collectHeight = 20



#DO NOT EDIT ME
pg.init()
width = 946
height = 455
screen = pg.display.set_mode((width,height))
clock = pg.time.Clock()
pg.display.set_caption('AABB Demo')
running = True
stage = 0a
fps = 500
coinHolder = []
framerates = []
backgroundIMG = pg.image.load('NicotineHotdog4.jpg')
backgroundRect = backgroundIMG.get_rect()
font = pg.font.Font('freesansbold.ttf', 32)


#Classes
class Player:
    def __init__(self, spawnX, spawnY, width, height):
        self.posV2 = [spawnX, spawnY]
        self.size = [width, height]
        self.score = 0
        self.XMin = self.posV2[0]
        self.XMax = self.posV2[0] + self.size[0]
        self.YMin = self.posV2[1]
        self.YMax = self.posV2[1] + self.size[1]

    def Movement(self, updateX, updateY):
        self.posV2[0] += updateX
        self.posV2[1] += updateY
        self.Update()
        #print(self.posV2)
        
    def Update(self):
        self.XMin = self.posV2[0]
        self.XMax = self.posV2[0] + self.size[0]
        self.YMin = self.posV2[1]
        self.YMax = self.posV2[1] + self.size[1]
        
    def DrawSelf(self, color):
        pg.draw.rect(screen, color, pg.Rect(self.posV2, self.size))
    
    def CheckCollisionsAABB(self, others):
        for other in others:
            if (self.XMin <= other.XMax and self.XMax >= other.XMin and self.YMin <= other.YMax and self.YMax >= other.YMin):
                self.score += other.value
                others.remove(other)
                return None
        #found both methods here: https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_collision_detection
    def CheckCollisionsBTS(self, others):
        for other in others:
            point = _GetClosestPoint(self, other)
            if (other.size[0]/2 > math.sqrt(((point[0] - other.posV2[0]) ** 2) + (point[1] - other.posV2[1]) ** 2)):
                    self.score += other.value
                    others.remove(other)

class Coin:
    def __init__(self, spawnX, spawnY, edgeLength, value = 1):
        self.posV2 = [spawnX, spawnY]
        self.size = [edgeLength, edgeLength]
        self.value = value
        self.XMin = self.posV2[0]
        self.XMax = self.posV2[0] + self.size[0]
        self.YMin = self.posV2[1]
        self.YMax = self.posV2[1] + self.size[1]
        self.counter = 0
        self.dirX = random.randint(-1,1)
        self.dirY = random.randint(-1,1)
        
    def __del__(self):
        print("Coin Grabbed")
    
    def Update(self):
        self.XMin = self.posV2[0]
        self.XMax = self.posV2[0] + self.size[0]
        self.YMin = self.posV2[1]
        self.YMax = self.posV2[1] + self.size[1]
    
    def Hover(self, dt, steps=fps, speed=40):
        if self.counter < steps:
            self.posV2[0] += (speed * dt) * self.dirX
            self.posV2[1] += (speed * dt) * self.dirY
        if self.counter > steps:
            self.counter = 0
            self.dirX = random.randint(-1,1)
            self.dirY = random.randint(-1,1)
        self.counter += 1
        
        self.Update()
            
        
    def DrawSelf(self, shape, color):
        if shape == 'Square':
            pg.draw.rect(screen, color, pg.Rect(self.posV2, self.size))
        if shape == 'Circle':
            pg.draw.circle(screen, color, self.posV2, self.size[0]/2)

        
#End Classes
        
#Functions
            
def clamp(val, cMin, cMax):
    if (val > cMin) and (val < cMax):
        return val
    elif (val < cMin):
        return cMin
    else:
        return cMax
    
def _GetClosestPoint(obj1, obj2):
  
    x = max(obj1.XMin, min(obj2.posV2[0], obj1.XMax))
    y = max(obj1.YMin, min(obj2.posV2[1], obj1.YMax))
    
    return[x, y]

def _KeepInBounds(OBJ):
    #Stay Right of the Left Side of the Screen
    if OBJ.posV2[0] < 0:
        OBJ.posV2[0] = 0
    #Stay Left of the Right Side of the Screen
    if OBJ.posV2[0] > width - OBJ.size[0]:
        OBJ.posV2[0] = width - OBJ.size[0]
    #Stay Under the Top Side of the Screen
    if OBJ.posV2[1] < 0:
        OBJ.posV2[1] = 0
    #Stay Over the Bottom Side of the Screen
    if OBJ.posV2[1] > height - OBJ.size[0]:
        OBJ.posV2[1] = height - OBJ.size[0]
        
        
def _GenerateCollectable(amt=5):
    for x in range(0, amt):
        coinHolder.append(Coin(random.randint(20, 920), random.randint(20, 445), 20))
        
def _UpdateScore(Stage, ScoreValue):
    score = ScoreValue
    stage = Stage
    #Score print out  https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
    text = font.render('Score: ' + str(score), True, 'white')
 
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
     
    # set the center of the rectangular object.
    textRect.center = (65, 20)
    screen.blit(text, textRect)
    if score >= 10:
        stage = 1
    if score >= 20:
        stage = 2
    if score >= 30:
        stage = 3
    return stage

def _PrintFrameRate():
    text = font.render('FPS: ' + str(int(clock.get_fps())), True, 'white')
 
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
     
    # set the center of the rectangular object.
    textRect.center = (width - 80,  20)
    screen.blit(text, textRect)
    
def _CalcAvgFrameRate():
    runningTotal = 0
    framerates.append(int(clock.get_fps()))
    
    for framerate in framerates:
        runningTotal += framerate
        
    avgFPS = runningTotal/len(framerates)
    
    text = font.render('AVG_FPS: ' + str(int(avgFPS)), True, 'white')
 
    # create a rectangular object for the
    # text surface object
    textRect = text.get_rect()
     
    # set the center of the rectangular object.
    textRect.center = (width - 121,  45)
    screen.blit(text, textRect)
    #print(avgFPS)
    
#End Functions
        
#Construct our Player Square       
Player1 = Player((width/2) - 10, (height/2) - 10, playerWidth, playerHeight)
#Generate the Initial Coins
_GenerateCollectable(10)

#Run Pygame from https://www.pygame.org/docs/
while running:
    dt = clock.tick(fps) / 1000
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    if len(coinHolder) == 0:
        _GenerateCollectable(10)
        
    # fill the screen with a color to wipe away anything from last frame
    if stage == 0:
        screen.fill("black")
    if stage == 1:
        screen.fill("grey")
    if stage == 2:
        screen.fill("red")
    if stage == 3:
        screen.fill("black")
    if Player1.score > 69:
        pass
        #screen.blit(backgroundIMG, backgroundRect)

    # RENDER YOUR GAME HERE
    Player1.DrawSelf('Blue')
    
    
    #Input Handling
    moveValueY = 0
    moveValueX = 0
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        moveValueY -= dt * ((speed + stage*.5) * 100)
    if keys[pg.K_s]:
        moveValueY += dt * ((speed + stage*.5) * 100)
    if keys[pg.K_a]:
        moveValueX -= dt * ((speed + stage*.5) * 100)
    if keys[pg.K_d]:
        moveValueX += dt * ((speed + stage*.5) * 100)
    
    Player1.Movement(moveValueX, moveValueY)
    _KeepInBounds(Player1)
    for coin in coinHolder:
        if ((stage == 2) or (stage == 3)):
            coin.Hover(dt)
        _KeepInBounds(coin)
        if ((stage == 0) or (stage == 2)):
            coin.DrawSelf('Square','Yellow')
            Player1.CheckCollisionsAABB(coinHolder)
        if ((stage == 1) or (stage == 3)):
            coin.DrawSelf('Circle','Yellow')
            Player1.CheckCollisionsBTS(coinHolder)

    stage = _UpdateScore(stage, Player1.score)
    _PrintFrameRate()
    #_CalcAvgFrameRate()
    # flip() the display to put your work on screen
    pg.display.flip()
    

pg.quit()