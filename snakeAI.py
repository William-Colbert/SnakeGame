#Imports needed for project
import numpy as np
import pygame as pg
import random
import math
import sys

pg.init()
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
        self.direction = 3
        self.lastMove = 1
        self.gameOver = False
        self.appleImg = pg.image.load('SnakeGame/assets/apple.png').convert_alpha()
        self.app = self.spawnApple(self.snakeDict, self.appleImg)
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
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3
        clockwise = [RIGHT, DOWN, LEFT, UP]

        if np.array_equal(action, [1,0,0]):
            newDir = self.direction
        elif np.array_equal(action, [0,1,0]):
            newDir = (self.direction + 1) % 4
        else:
            newDir = (self.direction - 1) % 4
        self.direction = newDir
    
        head = snake.get(0)
        self.partnerOldRow = head.row
        self.partnerOldCol = head.col
        if self.direction == 3:
            head.row -= 1
        elif self.direction == 1:
            head.row += 1
        elif self.direction == 2:
            head.col -= 1
        elif self.direction == 0:
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

    def checkGameOver(self, snake, action):
        head = snake.get(0)
        if action == 3 and head.row - 1 < 0:
            return True
        elif action == 1 and head.row + 1 > 9:
            return True
        elif action == 2 and head.col - 1 < 0:
            return True
        elif action == 0 and head.col + 1 > 9:
            return True
        
        for obj in snake:
            self.current = snake[obj]
            if head.col - 1 == self.current.col and head.row == self.current.row and action == 2:
                return True
            if head.col + 1 == self.current.col and head.row == self.current.row and action == 0:
                return True
            if head.col == self.current.col and head.row - 1 == self.current.row and action == 3:
                return True
            if head.col == self.current.col and head.row + 1 == self.current.row and action == 1:
                return True
        
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
        self.frame_iteration += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
        self.direction = action
        self.screen.fill("seagreen")
        self.drawSquares()
        self.drawBoard(self.snakeDict, self.screen)
        reward = 0
        if self.app:
            self.app.draw(self.screen)
        else:
            self.app = self.spawnApple(self.snakeDict, self.appleImg)
        self.ticks = pg.time.get_ticks()
        if self.ticks > self.timer:
            self.timer += 250
            if not self.gameOver:
                self.gameOver = self.checkGameOver(self.snakeDict, action)
            if not self.gameOver:
                self.snakeDict = self.updateBoard(self.snakeDict, action)
                self.lastMove = self.direction
                if self.collectApple(self.snakeDict, self.app):
                    reward += 10
                    self.app = self.spawnApple(self.snakeDict, self.appleImg)
                    self.score += 1
                    self.snakeDict = self.growSnake(self.snakeDict, self.id, self.bodyImg)
                    self.id += 1
                    print(self.score)
                else:
                    reward -= 0.1
            if self.gameOver or self.frame_iteration > 100*len(self.snakeDict):
                reward -= 10
                self.reset()
                return reward, self.gameOver, self.score
        
        pg.display.flip()
        self.clock.tick(10)
        return reward, self.gameOver, self.score