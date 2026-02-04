#Imports needed for project
import numpy as np
import pygame as pg
import math
import sys

#Classes
class head():
    def __init__(self, row, col, image):
        self.row = row
        self.col = col
        self.image = image

    def draw(self):
        x = 161 + self.col * 70
        y = 30 + self.row * 70
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        screen.blit(self.image, (x,y))

class body():
    def __init__(self, row, col, image):
        self.row = row
        self.col = col
        self.image = image

    def draw(self):
        x = 161 + self.col * 70
        y = 30 + self.row * 70
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        screen.blit(self.image, (x,y))

class apple():
    def __init__(self, row, col, image):
        self.row = row
        self.col = col
        self.image = image
        
    def draw(self):
        x = 161 + self.col * 70
        y = 30 + self.row * 70
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        screen.blit(self.image, (x,y))


#Functions
def drawSquares():
    #Starting position of first square and size of all squares
    xPos = 150
    yPos = 650
    sqSize = 70


    #Draw squares on snakeBoard
    darkSquare = True
    for i in range(100):
        R = pg.Rect(xPos,yPos,sqSize,sqSize)

        if i % 2 == 0 and darkSquare:
            pg.draw.rect(screen, "olivedrab", R, width == 0)
        elif i % 2 == 0 and not darkSquare:
            pg.draw.rect(screen, "olive", R, width == 0)
        elif i % 2 == 1 and darkSquare:
            pg.draw.rect(screen, "olive", R, width == 0)
        else:
            pg.draw.rect(screen, "olivedrab", R, width == 0)

        if (i+1) % 10 == 0:
            xPos = 150
            yPos -= 70
            darkSquare = not darkSquare
        else:
            xPos += 70

def setupHead():
    img = pg.image.load('SnakeGame/assets/snakeHead.png').convert_alpha()
    h = head(8, 4, img)
    return h

def drawBoard(snakeD):
    for obj in snakeD:
        snakeD[obj].draw()

def updateBoard(snake, dir):
    head = snake.get(0)
    partnerOldRow = head.row
    partnerOldCol = head.col
    if dir == "up":
        head.row -= 1
    elif dir == "down":
        head.row += 1
    elif dir == "left":
        head.col -= 1
    elif dir == "right":
        head.col += 1

    for obj in snake:
        myID = obj
        if myID != 0:
            myOldRow = snake[obj].row
            myOldCol = snake[obj].col

            snake[obj].row = partnerOldRow
            snake[obj].col = partnerOldCol

            partnerOldRow = myOldRow
            partnerOldCol = myOldCol

    return snake
#Start of Main Code
#Initialize Screen
pg.init()
timer = 300
size = width, height = 1000, 750
screen = pg.display.set_mode(size)
clock = pg.time.Clock()
snakeHead = setupHead()
bodyImg = pg.image.load('SnakeGame/assets/snakeBody.png').convert_alpha()
snakeBody = body(9, 4, bodyImg)
snakeDict = {0: snakeHead,
             1: snakeBody}
direction = "up"

#Do gameplay loop forever, close when X is clicked
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                direction = "up"
            if event.key == pg.K_a:
                direction = "left"
            if event.key == pg.K_s:
                direction = "down"
            if event.key == pg.K_d:
                direction = "right"

    screen.fill("seagreen")
    drawSquares()
    drawBoard(snakeDict)
    ticks = pg.time.get_ticks()
    if ticks > timer:
        timer += 300
        snakeDict = updateBoard(snakeDict, direction)
    
    pg.display.flip()
    clock.tick(60)