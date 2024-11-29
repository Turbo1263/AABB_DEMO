#Mason Bledsoe 2D Collision Detection 11.22.2024
import pygame as pg
import random
import math

pg.init()
width = 946
height = 455
screen = pg.display.set_mode((width,height))
clock = pg.time.Clock()
pg.display.set_caption('AABB Demo')
running = True
stage = 0
coinHolder = []
framerates = []
backgroundIMG = pg.image.load('NicotineHotdog4.jpg')
backgroundRect = backgroundIMG.get_rect()
font = pg.font.Font('freesansbold.ttf', 32)


#Classes
class Player:
    def __init__(self, spawnX, spawnY, edgeLength):
        self.posV2 = [spawnX, spawnY]
        self.size = [edgeLength, edgeLength]
        self.score = 0
    
    def Movement(self, updateX, updateY):
        self.posV2[0] += updateX
        self.posV2[1] += updateY
        #print(self.posV2)
        
    def DrawSelf(self, color):
        pg.draw.rect(screen, color, pg.Rect(self.posV2, self.size))
    
    def CheckCollisionsAABB(self, others):
        for other in others:
            if (self.posV2[0] > other.posV2[0]) and (self.posV2[0] < other.posV2[0] + other.size[0]):
                if (self.posV2[1] > other.posV2[1]) and (self.posV2[1] < other.posV2[1] + other.size[1]):
                    self.score += other.value
                    others.remove(other)
                    return None
            if (self.posV2[0] + self.size[0] > other.posV2[0]) and (self.posV2[0] + 20 < other.posV2[0] + other.size[0]):
                if (self.posV2[1] > other.posV2[1]) and (self.posV2[1] < other.posV2[1] + other.size[1]):
                    self.score += other.value
                    others.remove(other)
                    return None
            if (self.posV2[0] > other.posV2[0]) and (self.posV2[0] < other.posV2[0] + other.size[0]):
                if (self.posV2[1] + self.size[1]  > other.posV2[1]) and (self.posV2[1] + self.size[1]  < other.posV2[1] + other.size[1]):
                    self.score += other.value
                    others.remove(other)
                    return None
            if (self.posV2[0] + self.size[0]  > other.posV2[0]) and (self.posV2[0] + self.size[0]  < other.posV2[0] + other.size[0]):
                if (self.posV2[1] + self.size[1]  > other.posV2[1]) and (self.posV2[1] + self.size[1]  < other.posV2[1] + other.size[1]):
                    self.score += other.value
                    others.remove(other)
                    return None
    def CheckCollisionsBTS(self, others):
        for other in others:
            if (other.size[0]/2 > math.sqrt(((self.posV2[0] - other.posV2[0]) ** 2) + (self.posV2[1] - other.posV2[1]) ** 2)):
                    self.score += other.value
                    others.remove(other)
                    return None
            if (other.size[0]/2 > math.sqrt((((self.posV2[0]+self.size[0]) - other.posV2[0]) ** 2) + (self.posV2[1] - other.posV2[1]) ** 2)):
                    self.score += other.value
                    others.remove(other)
                    return None
            if (other.size[0]/2 > math.sqrt(((self.posV2[0] - other.posV2[0]) ** 2) + ((self.posV2[1]+self.size[0]) - other.posV2[1]) ** 2)):
                    self.score += other.value
                    others.remove(other)
                    return None
            if (other.size[0]/2 > math.sqrt((((self.posV2[0]+self.size[0]) - other.posV2[0]) ** 2) + ((self.posV2[1]+self.size[0]) - other.posV2[1]) ** 2)):
                    self.score += other.value
                    others.remove(other)
                    return None
                    
class Coin:
    def __init__(self, spawnX, spawnY, edgeLength, value = 1):
        self.posV2 = [spawnX, spawnY]
        self.size = [edgeLength, edgeLength]
        self.value = value
        
    def __del__(self):
        print("Coin Grabbed")
        
    def DrawSelf(self, shape, color):
        if shape == 'Square':
            pg.draw.rect(screen, color, pg.Rect(self.posV2, self.size))
        if shape == 'Circle':
            pg.draw.circle(screen, color, self.posV2, self.size[0]/2)

        
#End Classes
        
#Functions
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
    if score >= 15:
        stage = 1
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
Player1 = Player((width/2) - 10, (height/2) - 10, 20)
#Generate the Initial Coins
_GenerateCollectable()

#Run Pygame from https://www.pygame.org/docs/
while running:
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
    if Player1.score > 69:
        screen.blit(backgroundIMG, backgroundRect)

    # RENDER YOUR GAME HERE
    Player1.DrawSelf('Blue')
    
    
    #Input Handling
    moveValueY = 0
    moveValueX = 0
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        moveValueY -= 100 * dt
    if keys[pg.K_s]:
        moveValueY += 100 * dt
    if keys[pg.K_a]:
        moveValueX -= 100 * dt
    if keys[pg.K_d]:
        moveValueX += 100 * dt
    
    Player1.Movement(moveValueX, moveValueY)
    _KeepInBounds(Player1)
    if stage == 0:
        #print(stage)
        for coin in coinHolder:
            coin.DrawSelf('Square','Yellow')
        Player1.CheckCollisionsAABB(coinHolder)
    if stage == 1:
        #print(stage)
        for coin in coinHolder:
            coin.DrawSelf('Circle','Yellow')
        Player1.CheckCollisionsBTS(coinHolder)

    stage = _UpdateScore(stage, Player1.score)
    _PrintFrameRate()
    #_CalcAvgFrameRate()
    # flip() the display to put your work on screen
    pg.display.flip()
    dt = clock.tick(500) / 1000

pg.quit()