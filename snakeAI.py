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
        self.snakeHead = self.setupHead()
        self.bodyImg = pg.image.load('SnakeGame/assets/snakeBody.png').convert_alpha()
        self.snakeBody = self.body(9, 4, self.bodyImg)
        self.snakeDict = {0: self.snakeHead,
                    1: self.snakeBody}
        self.direction = "up"
        self.lastMove = "down"
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

    def setupHead(self):
        img = pg.image.load('SnakeGame/assets/snakeHead.png').convert_alpha()
        h = self.head(8, 4, img)
        return h

    def drawBoard(self, snakeD, screen):
        for obj in snakeD:
            snakeD[obj].draw(screen)

    def updateBoard(self, snake, dir):
        self.head = snake.get(0)
        self.partnerOldRow = self.head.row
        self.partnerOldCol = self.head.col
        if dir == "up":
            self.head.row -= 1
        elif dir == "down":
            self.head.row += 1
        elif dir == "left":
            self.head.col -= 1
        elif dir == "right":
            self.head.col += 1

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

    def checkGameOver(self, snake, dir):
        self.head = snake.get(0)
        if dir == "up" and self.head.row - 1 < 0:
            return True
        elif dir == "down" and self.head.row + 1 > 9:
            return True
        elif dir == "left" and self.head.col - 1 < 0:
            return True
        elif dir == "right" and self.head.col + 1 > 9:
            return True
        
        for obj in snake:
            self.current = snake[obj]
            if self.head.col - 1 == self.current.col and self.head.row == self.current.row and dir == "left":
                return True
            if self.head.col + 1 == self.current.col and self.head.row == self.current.row and dir == "right":
                return True
            if self.head.col == self.current.col and self.head.row - 1 == self.current.row and dir == "up":
                return True
            if self.head.col == self.current.col and self.head.row + 1 == self.current.row and dir == "down":
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
        self.head = snake.get(0)
        if self.head.row == app.row and self.head.col == app.col:
            return True
        return False

    def growSnake(self, snake, dir, id, img):
        self.lastBody = snake.get(len(snake) - 1)
        self.canGrowLeft = True
        self.canGrowRight = True
        self.canGrowUp = True
        self.canGrowDown = True
        for obj in snake:
            self.current = snake[obj]
            if self.lastBody.col - 1 == self.current.col and self.lastBody.row == self.current.row or self.lastBody.col - 1 < 0:
                canGrowLeft = False
            if self.lastBody.col + 1 == self.current.col and self.lastBody.row == self.current.row or self.lastBody.col + 1 > 9:
                canGrowRight = False
            if self.lastBody.col == self.current.col and self.lastBody.row - 1 == self.current.row or self.lastBody.row - 1 < 0:
                canGrowUp = False
            if self.lastBody.col == self.current.col and self.lastBody.row + 1 == self.current.row or self.lastBody.row + 1 > 9:
                canGrowDown = False

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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    if self.lastMove != "down":
                        self.direction = "up"
                if event.key == pg.K_a:
                    if self.lastMove != "right":
                        self.direction = "left"
                if event.key == pg.K_s:
                    if self.lastMove != "up":
                        self.direction = "down"
                if event.key == pg.K_d:
                    if self.lastMove != "left":
                        self.direction = "right"

        self.screen.fill("seagreen")
        self.drawSquares()
        self.drawBoard(self.snakeDict, self.screen)
        if self.app:
            self.app.draw(self.screen)
        else:
            self.app = self.spawnApple(self.snakeDict, self.appleImg)
        self.ticks = pg.time.get_ticks()
        if self.ticks > self.timer:
            self.timer += 250
            if not self.gameOver:
                self.gameOver = self.checkGameOver(self.snakeDict, self.direction)
            if not self.gameOver:
                self.snakeDict = self.updateBoard(self.snakeDict, self.direction)
                self.lastMove = self.direction
                if self.collectApple(self.snakeDict, self.app):
                    self.app = None
                    self.score += 1
                    self.snakeDict = self.growSnake(self.snakeDict, self.lastMove, self.id, self.bodyImg)
                    self.id += 1
                    print(self.score)
        
        pg.display.flip()
        self.clock.tick(60)
        return self.gameOver, self.score
if __name__ == '__main__':
    game = snakeGameAI()

    while True:
        gameOver, score = game.playStep()

        if gameOver == True:
            break
    print('Final Score:', score)

    pg.quit()