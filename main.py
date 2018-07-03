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

from networkmodel import DeviceModel

from random import randint
import random
import os

activeScreen = None


def main():
    pygame.init()
    
    fpsClock = pygame.time.Clock()

    screen = pygame.display.set_mode((1280,720))
    workSurface = pygame.Surface((1280,720))
    shaderSurface = pygame.Surface((1280,720))

    crtTile = pygame.image.load(os.path.join('res','image','crtsim_scanlines.png'))
    crtTile = pygame.transform.scale(crtTile, (20, 10))
    crtPixelShader = OverlayShader(crtTile)

    global activeScreen
    
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        loggingInTransition.resetAnimation()
                        activeScreen = loggingInTransition
                        transitionCounter = 30
            #check for a device connected
        elif activeScreen == loggingInTransition:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            transitionCounter -= 1
            if transitionCounter <= 0:
                transitionCounter = 0
                loggedInScreen.reset()
                loggedInScreen.sendLineToTerminal("STATUS: ARTIFACT CONNECTED.")
                loggedInScreen.sendLineToTerminal("DECRYPTION PROGRESS: 5/8")
                activeScreen = loggedInScreen
            
        elif activeScreen == loggedInScreen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        loggedInScreen.textBoxBackspace()
                    elif event.key == pygame.K_RETURN:
                        loggedInScreen.sendLineToTerminal("TRYING PASSWORD: " + loggedInScreen.getPassword())
                        loggedInScreen.sendLineToTerminal("PASSWORD ACCEPTED. UNLOCKING RUNE.")
                        loggedInScreen.sendLineToTerminal("DECRYPTION PROGRESS")
                        #gameManager.consumePassword(loggedInScreen.getPassword())
                        loggedInScreen.clearTextBox()
                    elif event.key == pygame.K_SPACE:
                        activeScreen = loggedOutScreen
                    else:
                        loggedInScreen.sendKeyToTextBox(event.unicode.upper())
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        workSurface.fill(colors.green_bg)
        activeScreen.draw(workSurface)


        shaderSurface.blit(workSurface, (0,0)) 
        # shaderSurface = blurShader.apply(shaderSurface)
        shaderSurface = crtPixelShader.apply(shaderSurface)

        screen.blit(shaderSurface, (0,0))
        pygame.display.update()
        fpsClock.tick(60)

        

if __name__=="__main__":
    main()
