#Mason Bledsoe 2D Collision Detection 11.22.2024
import pygame as pg
import random

pg.init()
width = 640
height = 480
screen = pg.display.set_mode((width,height))
clock = pg.time.Clock()
running = True
numCoins = 0
coinHolder = []

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
    
    def CheckCollisions(self, others):
        for other in others:
            if (self.posV2[0] > other.posV2[0]) and (self.posV2[0] < other.posV2[0] + other.size[0]):
                if (self.posV2[1] > other.posV2[1]) and (self.posV2[1] < other.posV2[1] + other.size[1]):
                    self.score += other.value
                    others.remove(other)
                    return None
            if (self.posV2[0] + 20 > other.posV2[0]) and (self.posV2[0] + 20 < other.posV2[0] + other.size[0]):
                if (self.posV2[1] > other.posV2[1]) and (self.posV2[1] < other.posV2[1] + other.size[1]):
                    self.score += other.value
                    others.remove(other)
                    return None
            if (self.posV2[0] > other.posV2[0]) and (self.posV2[0] < other.posV2[0] + other.size[0]):
                if (self.posV2[1] + 20 > other.posV2[1]) and (self.posV2[1] + 20 < other.posV2[1] + other.size[1]):
                    self.score += other.value
                    others.remove(other)
                    return None
            if (self.posV2[0] + 20 > other.posV2[0]) and (self.posV2[0] + 20 < other.posV2[0] + other.size[0]):
                if (self.posV2[1] + 20 > other.posV2[1]) and (self.posV2[1] + 20 < other.posV2[1] + other.size[1]):
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
        
    def DrawSelf(self, color):
        pg.draw.rect(screen, color, pg.Rect(self.posV2, self.size))
        
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
        
        
def _GenerateCoins(amt=5):
    for x in range(0, amt):
        coinHolder.append(Coin(random.randint(20, 620), random.randint(20, 460), 20))   
#End Functions
        
#Construct our Player Square       
Player1 = Player((width/2) - 10, (height/2) - 10, 20)
_GenerateCoins()

#Run Pygame from https://www.pygame.org/docs/
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    if len(coinHolder) == 0:
        _GenerateCoins(10)
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    Player1.DrawSelf('Red')
    for coin in coinHolder:
        coin.DrawSelf('Yellow')
    
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
    Player1.CheckCollisions(coinHolder)
    # flip() the display to put your work on screen
    pg.display.flip()
    print(Player1.score)
    dt = clock.tick(60) / 1000

pg.quit()