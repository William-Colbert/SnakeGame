#Imports needed for project
import numpy as np
import pygame as pg
import random
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

def checkGameOver(snake, dir):
    head = snake.get(0)
    if dir == "up" and head.row - 1 < 0:
        return True
    elif dir == "down" and head.row + 1 > 9:
        return True
    elif dir == "left" and head.col - 1 < 0:
        return True
    elif dir == "right" and head.col + 1 > 9:
        return True
    
    for obj in snake:
        current = snake[obj]
        if head.col - 1 == current.col and head.row == current.row and dir == "left":
            return True
        if head.col + 1 == current.col and head.row == current.row and dir == "right":
            return True
        if head.col == current.col and head.row - 1 == current.row and dir == "up":
            return True
        if head.col == current.col and head.row + 1 == current.row and dir == "down":
            return True
    
    return False

def spawnApple(snake, img):
    while True:
        canSpawn = True
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        for obj in snake:
            currentPart = snake[obj]
            if row == currentPart.row and col == currentPart.col:
                canSpawn = False
                break
        if canSpawn:
            return apple(row, col, img)

def collectApple(snake, app):
    head = snake.get(0)
    if head.row == app.row and head.col == app.col:
        return True
    return False

def growSnake(snake, dir, id, img):
    lastBody = snake.get(len(snake) - 1)
    canGrowLeft = True
    canGrowRight = True
    canGrowUp = True
    canGrowDown = True
    for obj in snake:
        current = snake[obj]
        if lastBody.col - 1 == current.col and lastBody.row == current.row or lastBody.col - 1 < 0:
            canGrowLeft = False
        if lastBody.col + 1 == current.col and lastBody.row == current.row or lastBody.col + 1 > 9:
            canGrowRight = False
        if lastBody.col == current.col and lastBody.row - 1 == current.row or lastBody.row - 1 < 0:
            canGrowUp = False
        if lastBody.col == current.col and lastBody.row + 1 == current.row or lastBody.row + 1 > 9:
            canGrowDown = False

    if canGrowLeft:
        snake[id] = body(lastBody.row, lastBody.col - 1, img)
        print("grow: " + str(id))
        return snake 
    if canGrowRight:
        snake[id] = body(lastBody.row, lastBody.col + 1, img)
        print("grow: " + str(id)) 
        return snake
    if canGrowUp:
        snake[id] = body(lastBody.row - 1, lastBody.col, img)
        print("grow: " + str(id)) 
        return snake
    if canGrowDown:
        snake[id] = body(lastBody.row + 1, lastBody.col, img)
        print("grow: " + str(id)) 
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
lastMove = "down"
gameOver = False
appleExists = False
appleImg = pg.image.load('SnakeGame/assets/apple.png').convert_alpha()
app = spawnApple(snakeDict, appleImg)
score = 0
id = 2

#Do gameplay loop forever, close when X is clicked
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                if lastMove != "down":
                    direction = "up"
            if event.key == pg.K_a:
                if lastMove != "right":
                    direction = "left"
            if event.key == pg.K_s:
                if lastMove != "up":
                    direction = "down"
            if event.key == pg.K_d:
                if lastMove != "left":
                    direction = "right"

    screen.fill("seagreen")
    drawSquares()
    drawBoard(snakeDict)
    if app:
        app.draw()
    else:
        app = spawnApple(snakeDict, appleImg)
    ticks = pg.time.get_ticks()
    if ticks > timer:
        timer += 300
        if not gameOver:
            gameOver = checkGameOver(snakeDict, direction)
        if not gameOver:
            snakeDict = updateBoard(snakeDict, direction)
            lastMove = direction
            if collectApple(snakeDict, app):
                app = None
                score += 1
                snakeDict = growSnake(snakeDict, lastMove, id, bodyImg)
                id += 1
                print(score)
    
    pg.display.flip()
    clock.tick(60)