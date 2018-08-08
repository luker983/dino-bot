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

# Screen Coordinates
# These vary based on screen
class Coords:
    # restart button
    replay_button = (720, 360)
    # top right of dinosaur
    dino = (487, 371)
    # top left of obstacle box
    obs_orig = (490, 370)
    # initial width and height of obstacle box
    obs_width = 105
    obs_height = 30
    # top left of gameplay area
    game_orig = (400, 262)
    # width and height of gameplay area
    game_width = 1030 
    game_height = 432 

def main():
    factor = 7 # adjusts obstacle width over time, higher value = slower scaling
    reset = 40 # if count_r reaches this value, game resets
    
    print("--- Dino Bot ---")
    print("Obstacle Box X Origin =", Coords.obs_orig[0])
    print("Obstacle Box Width =", Coords.obs_width)
    print("Speed Factor =", factor)
    
    try:
        while True:
            # two restarts to get window in focus
            click(Coords.replay_button)
            click(Coords.replay_button)
            # moves mouse out of the way
            click(Coords.game_orig)

            # restart counter
            count_r = 0
            # progression counter
            count_p = 0
         
            # check for obstacles, jump if obstacle is in obstacle box
            while True:
                # reset if game over
                if count_r == reset: 
                    break;
                # if obstacle box is not all white, jump
                if imageGrab((int(round(count_p / factor))))[0][1] != 247: 
                    jump()    
                    count_r = 0 

                count_r += 1 
                count_p += 1
                # print("reset counter =", count_r)
                # print("progression counter =", count_p)
    except KeyboardInterrupt:
        exit()
 
# Clicks restart button
def click(coord):
    pyautogui.click(coord)

# Makes dinosaur jump
def jump():
    pyautogui.keyDown('space')
    time.sleep(0.01)
    # print("Jump")
    pyautogui.keyUp('space')

# Grabs obstacle box, converts to grayscale, returns sum of pixels
def imageGrab(shift = 0):
    screenstr = 'screencapture -R' + str(Coords.obs_orig[0]) + ',' + str(Coords.obs_orig[1]) + ',' + str(Coords.obs_width + shift) + ',' + str(Coords.obs_height) + ' grab.png' 
    os.system(screenstr) 
    image = Image.open("grab.png")  
    grayscale = ImageOps.grayscale(image)
    a = array(grayscale.getcolors())
    time.sleep(0.02) 
    # print(a)
    return a

main()
