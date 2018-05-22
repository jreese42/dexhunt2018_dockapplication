#!/usr/bin/env python3

import pygame
import colors
from shapes import BorderRect
from shaders import BlurShader
from shaders import OverlayShader

from widgets import Meter
from widgets import TypewriterText
from widgets import TypewriterCode

from random import randint
import os

def main():
    pygame.init()
    
    fpsClock = pygame.time.Clock()

    screen = pygame.display.set_mode((1280,720))
    workSurface = pygame.Surface((1280,720))
    workSurface.fill(colors.green_bg)
    shaderSurface = pygame.Surface((1280,720))
    blurShader = BlurShader(3)

    crtTile = pygame.image.load(os.path.join('res','image','crtsim_scanlines.png'))
    crtTile = pygame.transform.smoothscale(crtTile, (20, 10))
    crtPixelShader = OverlayShader(crtTile)


    rect = BorderRect(400, 150)

    meters = []
    for idx in range(5):
        meters.append(Meter(50, 200, 10, 10))
        meters[idx].setValue(randint(0, 10))

    typewriterText = TypewriterText()
    typewriterText.animateText("This is a test text writer", 1)
    typewriterCode = TypewriterCode(20, 12, msPerChar=30)


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        rect.draw(workSurface, 100, 100, 2)
        for idx,meter in enumerate(meters):
            meter.draw(workSurface, 530 + idx*60, 100)
        typewriterText.draw(workSurface, 110, 110)
        typewriterCode.draw(workSurface, 530, 680)


        shaderSurface.blit(workSurface, (0,0)) 
        shaderSurface = blurShader.apply(shaderSurface)
        shaderSurface = crtPixelShader.apply(shaderSurface)

        screen.blit(shaderSurface, (0,0))
        pygame.display.flip()
        fpsClock.tick(60)
        

if __name__=="__main__":
    main()
