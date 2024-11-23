#Mason Bledsoe 2D Collision Detection 11.22.2024
import pygame as pg
import random

pg.init()
width = 640
height = 480
screen = pg.display.set_mode((width,height))
clock = pg.time.Clock()
running = True
#classes
class Player:
    def __init__(self, spawnX, spawnY, edgeLength):
        self.posV2 = [spawnX, spawnY]
        self.size = [edgeLength, edgeLength]
    
    def Movement(self, updateX, updateY):
        self.posV2[0] += updateX
        self.posV2[1] += updateY
        
    def _DrawPlayer(self, color):
        pg.draw.rect(screen, color, pg.Rect(self.posV2, self.size))
class Coin:
    def __init__(self, spawnX, spawnY, value):
        self.posV2 = [spawnX, spawnY]
        self.value = value
        

#Construct our Player Square       
Player1 = Player((width/2) - 10, (height/2) - 10, 20)

#Run Pygame from https://www.pygame.org/docs/
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    Player1._DrawPlayer('Red')
    
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
    # flip() the display to put your work on screen
    pg.display.flip()

    dt = clock.tick(60) / 1000

pg.quit()