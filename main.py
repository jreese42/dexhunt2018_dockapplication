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

from random import randint
import random
import os

def main():
    pygame.init()
    
    fpsClock = pygame.time.Clock()

    screen = pygame.display.set_mode((1280,720))
    workSurface = pygame.Surface((1280,720))
    # workSurface.fill(colors.green_bg)
    shaderSurface = pygame.Surface((1280,720))
    blurShader = BlurShader(3)

    crtTile = pygame.image.load(os.path.join('res','image','crtsim_scanlines.png'))
    crtTile = pygame.transform.smoothscale(crtTile, (20, 10))
    crtPixelShader = OverlayShader(crtTile)

    def check_password(password):
        if password == "PASSWORD":
            for meter in meters:
                meter.setValue(10)
        else:
            for meter in meters:
                meter.setValue(random.choice(range(10)))

    rect = BorderRect(400, 150)

    meters = []
    for idx in range(5):
        meters.append(Meter(50, 200, 10, 10))
        meters[idx].setValue(randint(0, 10))

    typewriterText = TypewriterText()
    typewriterText.animateText("INPUT ENCRYPTION KEY", 1)
    typewriterCode = TypewriterCode(20, 12, msPerChar=30)
    textBox = TextBox()


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    textBox.setText(textBox.getText()[:-1])
                elif event.key == pygame.K_RETURN:
                    check_password(textBox.getText())
                    textBox.setText("")
                else:
                    textBox.setText(textBox.getText() + event.unicode.upper())

        workSurface.fill(colors.green_bg)
        rect.draw(workSurface, 100, 100, 2)
        for idx,meter in enumerate(meters):
            meter.draw(workSurface, 530 + idx*60, 100)
        typewriterText.draw(workSurface, 110, 110)
        typewriterCode.draw(workSurface, 530, 680)
        textBox.draw(workSurface, 155, 185)


        shaderSurface.blit(workSurface, (0,0)) 
        shaderSurface = blurShader.apply(shaderSurface)
        shaderSurface = crtPixelShader.apply(shaderSurface)

        screen.blit(shaderSurface, (0,0))
        pygame.display.update()
        fpsClock.tick(60)
        

if __name__=="__main__":
    main()
