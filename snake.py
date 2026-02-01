#Imports needed for project
import numpy as np
import pygame as pg
import math
import sys

#Classes


#Functions


#Start of Main Code
#Initialize Screen
pg.init()
size = width, height = 1000, 750
screen = pg.display.set_mode(size)
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
    
    #On title screen, show title image and start button
    #if gameState == "title":
    pg.display.flip()