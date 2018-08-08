##
# bot.py
# Bot to play Google's dinosaur game
#
# Luke Rindels
# August 6, 2018
##

from PIL import ImageOps, Image
import pyautogui
from numpy import *
import time
import os


factor = 8
reset = 60

# Screen Coordinates
class Coordinates:
    # restart button
    replay_button = (720, 360)
    # top right of dinosaur
    dino = (487 * 2, 371 * 2)
    # top left of obstacle box
    obs_orig = (490, 370)
    # bottom right of obstacle box
    obs_wh = (90, 20)
    # gameplay area
    game_orig = (400, 262)
    game_wh = (1030, 432)
    
# Clicks restart button
def restartGame():
    pyautogui.click(Coordinates.replay_button)

# Makes dinosaur jump
def jump():
    pyautogui.keyDown('space')
    time.sleep(0.05)
    # print("Jump")
    pyautogui.keyUp('space')

# Grabs obstacle box, converts to grayscale, returns sum of pixels
def imageGrab(shift = 0):
    screenstr = 'screencapture -R' + str(Coordinates.obs_orig[0]) + ',' + str(Coordinates.obs_orig[1]) + ',' + str(Coordinates.obs_wh[0] + shift) + ',' + str(Coordinates.obs_wh[1]) + ' grab.png' 
    os.system(screenstr) 
    image = Image.open("grab.png")  
    grayscale = ImageOps.grayscale(image)
    a = array(grayscale.getcolors())
    time.sleep(0.02) 
    # print(a)
    # print (a.sum())
    return a

# Game loop
print("--- Dino Bot ---")
print("X Origin =", Coordinates.obs_orig[0])
print("X Width =", Coordinates.obs_wh[0])
print("Speed Factor =", factor)
games = 1
while True:
    # two restarts to get window in focus
    restartGame()
    restartGame()
    time.sleep(1)
    # jump and initialize obstacle box
    jump()
    # restart counter
    x = 1
    # progression counter
    y = 1

    print("Games =", games)
    # check for obstacles, jump if obstacle is in obstacle box
    while True:
        # reset if game over
        if x == reset: 
            screenstr = 'screencapture -R' + str(Coordinates.game_orig[0]) + ',' + str(Coordinates.game_orig[1]) + ',' + str(Coordinates.game_wh[0]) + ',' + str(Coordinates.game_wh[1]) + ' game' + str(games) + '.png'
            os.system(screenstr) 
            games += 1
            break;
        if imageGrab((int(round(y / factor))))[0][1] != 247: 
            jump()
            x = 0
        x += 1 
        y += 1
        #print("x =", x)
        #print("y =", y) 
