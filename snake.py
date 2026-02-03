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


    #Draw squares on chessboard
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

def drawBoard(snakeBoard):
    #Start on black's side
    #Go through entire board and draw the current position
    for row in range(10):
        for col in range(10):
            object = snakeBoard[row][col]
            if object:
                object.draw()
                                        
    return snakeBoard

#Start of Main Code
#Initialize Screen
pg.init()
size = width, height = 1000, 750
screen = pg.display.set_mode(size)
snakeHead = setupHead()
bodyImg = pg.image.load('SnakeGame/assets/snakeBody.png').convert_alpha()
snakeBody = body(9, 4, bodyImg)
board = [[None]*10,
         [None]*10,
         [None]*10,
         [None]*10,
         [None]*10,
         [None]*10,
         [None]*10,
         [None]*10,
         [None, None, None, None, snakeHead, None, None, None, None, None],
         [None, None, None, None, snakeBody, None, None, None, None, None]
         ]
#gameState = "title"

#Create start button
#startImg = pg.image.load('ChessProject/ChessGame/assets/start.png').convert_alpha()
#startImg = pg.transform.scale_by(startImg, 0.2)
#startBtn = Button(317, 335, startImg)

#Create main menu button
#backImg = pg.image.load('ChessProject/ChessGame/assets/back.png').convert_alpha()
#backImg = pg.transform.scale_by(backImg, 0.1)
#backBtn = Button(740, 5, backImg)


#Do gameplay loop forever, close when X is clicked
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
    screen.fill("seagreen")
    drawSquares()
    board = drawBoard(board)
    #On title screen, show title image and start button
    #if gameState == "title":
    pg.display.flip()