import pygame
import colors
from shapes import BorderRect

import os
import collections
import random, string

pygame.font.init()
font_trs80 = pygame.font.Font(os.path.join('res','fonts','AnotherMansTreasureMIARaw.ttf'), 24)

#more ideas:
#loading bar
#decryptText
#text input
#ping spinner
#stone status (connected, num unlocked)

class TextBox:
    def __init__(this, maxlen=0):
        this.text = ""
        this.starttime = 0
        this.endtime = 0
        this.maxlen = maxlen

    def getText(this):
        return this.text

    def setText(this, text):
        this.text = text
        if this.maxlen != 0:
            this.text = this.text[0:this.maxlen]

    def draw(this, screen, x, y):
        cursor = ""
        if ( pygame.time.get_ticks() % 1500 ) < 750:
            cursor = "_"

        textSurface = font_trs80.render(this.text + cursor, 0, colors.green_fg)
        screen.blit(textSurface, (x,y))

class Meter:
    max_val = 0
    value = 0
    w = 0
    h = 0
    padding = 0
    subObjects = []
    def __init__(this, w, h, padding, max_val):
        this.subObjects.append(BorderRect(w, h))
        this.w = w
        this.h = h
        this.padding = padding
        this.max_val = max_val
        this.thiccness = 2

    def setValue(this, value):
        this.value = value
    
    def draw(this, screen, x, y):
        for obj in this.subObjects:
            obj.draw(screen, x, y, 2) #dont hardcode 2

        numBars = int((this.h / (this.padding + this.thiccness)) * (this.value / this.max_val))

        for idx in range(numBars):
            ypos = (idx * this.padding) + (idx * this.thiccness)
            ypos = y + this.h - ypos
            pygame.draw.line(screen, colors.green_fg, [x + this.padding, ypos], [x + this.w - this.padding, ypos], this.thiccness)

class TypewriterText:
    #wrap
    #timing manager
    #unblit
    #blinking cursor
    def __init__(this):
        this.text = ""
        this.starttime = 0
        this.endtime = 0

    def animateText(this, text, seconds, delay=0):
        this.text = text
        this.starttime = pygame.time.get_ticks() + (delay * 1000)
        this.duration = seconds*1000

    def draw(this, screen, x, y):
        tmpText = ""

        currtime = pygame.time.get_ticks()
        if (this.starttime != 0):
            numLetters = int(len(this.text) * (currtime - this.starttime) / (this.duration))
            tmpText = this.text[0:numLetters]

        tmpText += "_"

        textSurface = font_trs80.render(tmpText, 0, colors.green_fg)
        # backSurface = pygame.Surface(textSurface.get_size())
        # backSurface.fill(colors.green_bg)
        # screen.blit(backSurface, (x,y))
        screen.blit(textSurface, (x,y))

class TypewriterCode:
    numLines = 0
    fontSize = 0

    def __init__(this, numLines, fontSize, maxLineLen=80, msPerChar=600):
        this.numLines = numLines
        this.fontSize = fontSize
        this.textQueue = collections.deque(maxlen=numLines)
        this.msPerChar = msPerChar
        this.nextCharTime = pygame.time.get_ticks() + msPerChar
        this.lineSpacing = 2
        this.maxLineLen = maxLineLen
        # this.font = pygame.font.Font(os.path.join('res','fonts','AnotherMansTreasureMIARaw.ttf'), fontSize)
        this.font = pygame.font.Font(os.path.join('res','fonts','Iokharic.otf'), fontSize)
        this.tabLevel = 0
        this.newLineChance = 0.0

    def draw(this, screen, x, y):
        #write current line
        #if current line done, generate new line
        #first, draw all but the last line
        #typewriter effect
        #scroll correctly
        #unblit top line
        for idx,line in enumerate(this.textQueue):
            textSurface = this.font.render(line, 0, colors.green_fg)
            # backSurface = pygame.Surface(textSurface.get_size())
            # backSurface.fill(colors.green_bg)
            # screen.blit(backSurface, ( x, y - ((this.numLines - idx-1) * (this.lineSpacing + this.fontSize)) )) #clear old pos
            screen.blit(textSurface, ( x, y - (  (idx) * (this.lineSpacing + this.fontSize)) )) #fill new pos

        if pygame.time.get_ticks() > this.nextCharTime:
            this.nextCharTime = pygame.time.get_ticks() + this.msPerChar
            newLine = ""
            if random.uniform(0,1) < this.newLineChance:
                newLine = ""
                this.newLineChance = 0.0
            else:
                this.newLineChance += 0.008
                newLine = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(random.randint(this.maxLineLen / 4, this.maxLineLen)))
            this.textQueue.appendleft('  '*this.tabLevel + newLine)
            this.tabLevel += random.choice((-1, 1, 0, 0))
            if this.tabLevel > 0 and this.tabLevel <= 4:
                this.tabLevel += random.choice((-1, 1, 0, 0))
            elif this.tabLevel > 4:
                this.tabLevel += random.choice((-1, -1, 0, 0))
            elif this.tabLevel <= 0:
                this.tabLevel += random.choice((1, 1, 0, 0, 0))
        


