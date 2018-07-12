#!/usr/bin/env python3

import pygame
import colors
from shapes import BorderRect
from shaders import BlurShader
from shaders import OverlayShader

from widgets import TextBox
from widgets import Meter
from widgets import TypewriterText
from widgets import TypewriterCode

import screens
import GameManager

from random import randint
import random
import os
import string

def main():
    pygame.init()
    
    fpsClock = pygame.time.Clock()

    screen = pygame.display.set_mode((1280,720))
    workSurface = pygame.Surface((1280,720))
    shaderSurface = pygame.Surface((1280,720))

    crtTile = pygame.image.load(os.path.join('res','image','crtsim_scanlines.png'))
    crtTile = pygame.transform.scale(crtTile, (20, 10))
    crtPixelShader = OverlayShader(crtTile)

    activeScreen = None
    
    loggedOutScreen = screens.LoggedOutScreen()
    loggingInTransition = screens.LoggingInTransitionScreen()
    loggedInScreen = screens.LoggedInScreen()
    activeScreen = loggedOutScreen
    transitionCounter = 0

    gameManager = GameManager.GameManager()

    running = True
    while running:
        if activeScreen == loggedOutScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            #check for a device connected
            if gameManager.rfidTracker.rfidTagIsActive():
                loggingInTransition.resetAnimation()
                activeScreen = loggingInTransition
                transitionCounter = 30
        elif activeScreen == loggingInTransition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            transitionCounter -= 1
            if transitionCounter <= 0:
                transitionCounter = 0
                loggedInScreen.reset()
                loggedInScreen.sendLineToTerminal("STATUS: ARTIFACT CONNECTED.")
                loggedInScreen.sendLineToTerminal("UID: " + gameManager.rfidTracker.getActiveUid())
                activeDevice = gameManager.getActiveDevice()
                if activeDevice is not None:
                    progress = device.getGameStatus()
                    loggedInScreen.sendLineToTerminal("DECRYPTION PROGRESS: " + str(progress) + "/8")
                activeScreen = loggedInScreen
            
        elif activeScreen == loggedInScreen:
            if not gameManager.rfidTracker.rfidTagIsActive():
                activeScreen = loggedOutScreen
            for event in pygame.event.get():
                #if event.type == pygame.QUIT:
                    #running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        loggedInScreen.textBoxBackspace()
                    elif event.key == pygame.K_RETURN:
                        if loggedInScreen.getPassword().lower() == "exitprogram":
                            running = False
                        loggedInScreen.sendLineToTerminal("TRYING PASSWORD: " + loggedInScreen.getPassword())
                        if (gameManager.consumePassword(loggedInScreen.getPassword())):
                            loggedInScreen.sendLineToTerminal("PASSWORD ACCEPTED. UNLOCKING RUNE.")
                            loggedInScreen.sendLineToTerminal("DECRYPTION PROGRESS")
                        else:
                            loggedInScreen.sendLineToTerminal("PASSWORD INVALID. TRY AGAIN.")
                        loggedInScreen.clearTextBox()
                    else:
                        if event.unicode.upper() in string.printable:
                            loggedInScreen.sendKeyToTextBox(event.unicode.upper())
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        workSurface.fill(colors.green_bg)
        activeScreen.draw(workSurface)


        shaderSurface.blit(workSurface, (0,0)) 
        shaderSurface = crtPixelShader.apply(shaderSurface)

        screen.blit(shaderSurface, (0,0))
        pygame.display.update()
        fpsClock.tick(60)

        

if __name__=="__main__":
    main()
