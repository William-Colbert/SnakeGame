#Imports needed for project
import numpy as np
import pygame as pg
import random
from enum import Enum
import math
import sys

pg.init()
class Direction(Enum):
        RIGHT = 1
        LEFT = 2
        UP = 3
        DOWN = 4

class snakeGameAI():

    
    class head():
        def __init__(self, row, col, image):
            self.row = row
            self.col = col
            self.image = image

        def draw(self, screen):
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

        def draw(self, screen):
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
            
        def draw(self, screen):
            x = 161 + self.col * 70
            y = 30 + self.row * 70
            self.rect = self.image.get_rect()
            self.rect.topleft = (x,y)
            screen.blit(self.image, (x,y))

    def __init__(self, w=1000, h=750):
        self.w = w
        self.h = h

        self.size = width, height = w, h
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_caption('Snake')
        self.clock = pg.time.Clock()
        self.reset()

    def reset(self):
        self.timer = 250
        self.headImg = pg.image.load('SnakeGame/assets/snakeHead.png').convert_alpha()
        self.bodyImg = pg.image.load('SnakeGame/assets/snakeBody.png').convert_alpha()
        self.snakeHead = self.head(8, 4, self.headImg)
        self.snakeBody = self.body(9, 4, self.bodyImg)
        self.snakeDict = {0: self.snakeHead,
                    1: self.snakeBody}
        self.direction = Direction.UP
        self.lastMove = Direction.DOWN
        self.gameOver = False
        self.appleImg = pg.image.load('SnakeGame/assets/apple.png').convert_alpha()
        self.app = self.spawnApple(self.snakeDict, self.appleImg)
        self.oldDistance = abs(self.app.row - self.snakeDict.get(0).row) + abs(self.app.col - self.snakeDict.get(0).col)
        self.score = 0
        self.id = 2
        self.frame_iteration = 0


    #Functions
    def drawSquares(self):
        #Starting position of first square and size of all squares
        xPos = 150
        yPos = 650
        sqSize = 70


        #Draw squares on snakeBoard
        darkSquare = True
        for i in range(100):
            R = pg.Rect(xPos,yPos,sqSize,sqSize)

            if i % 2 == 0 and darkSquare:
                pg.draw.rect(self.screen, "olivedrab", R)
            elif i % 2 == 0 and not darkSquare:
                pg.draw.rect(self.screen, "olive", R)
            elif i % 2 == 1 and darkSquare:
                pg.draw.rect(self.screen, "olive", R)
            else:
                pg.draw.rect(self.screen, "olivedrab", R)

            if (i+1) % 10 == 0:
                xPos = 150
                yPos -= 70
                darkSquare = not darkSquare
            else:
                xPos += 70

    def drawBoard(self, snakeD, screen):
        for obj in snakeD:
            snakeD[obj].draw(screen)

    def updateBoard(self, snake, action):
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            newDir = clockwise[idx]
        elif np.array_equal(action, [0,1,0]):
            nextIdx = (idx + 1) % 4
            newDir = clockwise[nextIdx]
        else:
            nextIdx = (idx - 1) % 4
            newDir = clockwise[nextIdx]

        self.direction = newDir
    
        head = snake.get(0)
        self.partnerOldRow = head.row
        self.partnerOldCol = head.col
        if self.direction == Direction.UP:
            head.row -= 1
        elif self.direction == Direction.DOWN:
            head.row += 1
        elif self.direction == Direction.LEFT:
            head.col -= 1
        elif self.direction == Direction.RIGHT:
            head.col += 1

        for obj in snake:
            self.myID = obj
            if self.myID != 0:
                self.myOldRow = snake[obj].row
                self.myOldCol = snake[obj].col

                snake[obj].row = self.partnerOldRow
                snake[obj].col = self.partnerOldCol

                self.partnerOldRow = self.myOldRow
                self.partnerOldCol = self.myOldCol

        return snake

    def checkGameOver(self, snake):
        head = snake.get(0)
        #if action == Direction.UP and head.row - 1 < 0:
         #   return True
        #elif action == Direction.DOWN and head.row + 1 > 9:
         #   return True
        #elif action == Direction.LEFT and head.col - 1 < 0:
         #   return True
        #elif action == Direction.RIGHT and head.col + 1 > 9:
         #   return True

        if head.row > 9 or head.row < 0 or head.col > 9 or head.col < 0:
            return True
        
        for obj in snake:
            self.current = snake[obj]
            if head.col == self.current.col and head.row == self.current.row and self.current != snake[0]:
                return True
            #if head.col - 1 == self.current.col and head.row == self.current.row and action == Direction.LEFT:
             #   return True
            #if head.col + 1 == self.current.col and head.row == self.current.row and action == Direction.RIGHT:
             #   return True
            #if head.col == self.current.col and head.row - 1 == self.current.row and action == Direction.UP:
             #   return True
            #if head.col == self.current.col and head.row + 1 == self.current.row and action == Direction.DOWN:
             #   return True
        
        return False

    def spawnApple(self, snake, img):
        while True:
            self.canSpawn = True
            self.row = random.randint(0, 9)
            self.col = random.randint(0, 9)
            for obj in snake:
                self.currentPart = snake[obj]
                if self.row == self.currentPart.row and self.col == self.currentPart.col:
                    self.canSpawn = False
                    break
            if self.canSpawn:
                return self.apple(self.row, self.col, img)

    def collectApple(self, snake, app):
        head = snake.get(0)
        if head.row == app.row and head.col == app.col:
            return True
        return False

    def growSnake(self, snake, id, img):
        self.lastBody = snake.get(len(snake) - 1)
        self.canGrowLeft = True
        self.canGrowRight = True
        self.canGrowUp = True
        self.canGrowDown = True
        for obj in snake:
            self.current = snake[obj]
            if self.lastBody.col - 1 == self.current.col and self.lastBody.row == self.current.row or self.lastBody.col - 1 < 0:
                self.canGrowLeft = False
            if self.lastBody.col + 1 == self.current.col and self.lastBody.row == self.current.row or self.lastBody.col + 1 > 9:
                self.canGrowRight = False
            if self.lastBody.col == self.current.col and self.lastBody.row - 1 == self.current.row or self.lastBody.row - 1 < 0:
                self.canGrowUp = False
            if self.lastBody.col == self.current.col and self.lastBody.row + 1 == self.current.row or self.lastBody.row + 1 > 9:
                self.canGrowDown = False

        if self.canGrowLeft:
            snake[id] = self.body(self.lastBody.row, self.lastBody.col - 1, img)
            print("grow: " + str(id))
            return snake 
        if self.canGrowRight:
            snake[id] = self.body(self.lastBody.row, self.lastBody.col + 1, img)
            print("grow: " + str(id)) 
            return snake
        if self.canGrowUp:
            snake[id] = self.body(self.lastBody.row - 1, self.lastBody.col, img)
            print("grow: " + str(id)) 
            return snake
        if self.canGrowDown:
            snake[id] = self.body(self.lastBody.row + 1, self.lastBody.col, img)
            print("grow: " + str(id)) 
            return snake

    
    #Do gameplay loop forever, close when X is clicked
    def playStep(self, action):
        reward = 0
        self.frame_iteration += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        self.screen.fill("seagreen")
        self.drawSquares()
        self.drawBoard(self.snakeDict, self.screen)
        #self.snakeDict = self.updateBoard(self.snakeDict, action)
        if self.app:
            self.app.draw(self.screen)
        else:
            self.app = self.spawnApple(self.snakeDict, self.appleImg)
        self.ticks = pg.time.get_ticks()
        if self.ticks > self.timer:
            self.timer += 250
            if not self.gameOver:
                self.gameOver = self.checkGameOver(self.snakeDict)
            if not self.gameOver:
                self.snakeDict = self.updateBoard(self.snakeDict, action)
                self.lastMove = self.direction
                newDistance = abs(self.app.row - self.snakeDict.get(0).row) + abs(self.app.col - self.snakeDict.get(0).col)
                if self.collectApple(self.snakeDict, self.app):
                    reward += 20
                    self.app = self.spawnApple(self.snakeDict, self.appleImg)
                    self.score += 1
                    self.snakeDict = self.growSnake(self.snakeDict, self.id, self.bodyImg)
                    self.id += 1
                    print(self.score)
                if self.oldDistance > newDistance:
                    reward += 1
                    self.oldDistance = newDistance
                elif self.oldDistance < newDistance:
                    reward -= 1
                    self.oldDistance = newDistance
            if self.gameOver or self.frame_iteration > 100*len(self.snakeDict):
                reward -= 5
                print(self.score)
                return reward, self.gameOver, self.score
        
        pg.display.flip()
        self.clock.tick(10)
        return reward, self.gameOver, self.score