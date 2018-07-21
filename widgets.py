import pygame
import colors
from shapes import BorderRect

import os
import collections
import random, string

pygame.font.init()
fonts = {
    '8' : pygame.font.Font(os.path.join('res','fonts','AnotherMansTreasureMIARaw.ttf'), 8),
    '10' : pygame.font.Font(os.path.join('res','fonts','AnotherMansTreasureMIARaw.ttf'), 10),
    '12' : pygame.font.Font(os.path.join('res','fonts','AnotherMansTreasureMIARaw.ttf'), 12),
    '16' : pygame.font.Font(os.path.join('res','fonts','AnotherMansTreasureMIARaw.ttf'), 16),
    '21' : pygame.font.Font(os.path.join('res','fonts','AnotherMansTreasureMIARaw.ttf'), 21),
    '24' : pygame.font.Font(os.path.join('res','fonts','AnotherMansTreasureMIARaw.ttf'), 24)
}
fonts_alien = {
    '8' : pygame.font.Font(os.path.join('res','fonts','Iokharic.otf'), 8),
    '10' : pygame.font.Font(os.path.join('res','fonts','Iokharic.otf'), 10),
    '12' : pygame.font.Font(os.path.join('res','fonts','Iokharic.otf'), 12),
    '16' : pygame.font.Font(os.path.join('res','fonts','Iokharic.otf'), 16),
    '21' : pygame.font.Font(os.path.join('res','fonts','Iokharic.otf'), 21),
    '24' : pygame.font.Font(os.path.join('res','fonts','Iokharic.otf'), 24)
}

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

        textSurface = fonts['24'].render(this.text + cursor, 0, colors.green_fg)
        screen.blit(textSurface, (x,y))

class Meter:
    max_val = 0
    value = 0
    w = 0
    h = 0
    padding = 0
    subObjects = []
    def __init__(this, w, h, padding, max_val, thiccness=2):
        this.w = w
        this.h = h
        this.padding = padding
        this.max_val = max_val
        this.thiccness = thiccness
        this.subObjects.append(BorderRect(w, h, this.thiccness))

    def setValue(this, value):
        this.value = value
    
    def draw(this, screen, x, y):
        for obj in this.subObjects:
            obj.draw(screen, x, y)

        numBars = int((this.h / (this.padding + this.thiccness)) * (float(this.value) / float(this.max_val)))

        for idx in range(numBars):
            ypos = (idx * this.padding) + (idx * this.thiccness)
            ypos = y + this.h - ypos
            pygame.draw.line(screen, colors.green_fg, [x + this.padding, ypos], [x + this.w - this.padding, ypos], this.thiccness)

class TypewriterText:
    #wrap
    #timing manager
    #unblit
    #blinking cursor
    def __init__(this, fontSize='24', fontstyle="console", delayAtEndOfLine=True):
        this.text = []
        this.starttime = 0
        this.endtime = 0
        this.currline = 0
        if (fontstyle is "console"):
            this.font=fonts.get(fontSize)
            if this.font is None:
                this.font = fonts.get('24')
                this.fontSize = 24
        elif (fontstyle is "alien"):
            this.font=fonts_alien.get(fontSize)
            if this.font is None:
                this.font = fonts_alien.get('24')
                this.fontSize = 24
        this.fontSize = int(fontSize)
        this.delayAtEndOfLine = delayAtEndOfLine

    def animateText(this, text, seconds, delay=0, drawBackground=False):
        this.text = text.split('\n')
        this.starttime = pygame.time.get_ticks() + (delay * 1000)
        this.duration = seconds*1000
        this.delay = delay*1000
        this.drawBackground = drawBackground

    def draw(this, screen, x, y):
        tmpText = ""


        if (this.currline < len(this.text)):
            #render the current line

            currtime = pygame.time.get_ticks()
            if (this.starttime != 0 and currtime >= this.starttime):
                numLetters = int(len(this.text[this.currline]) * (currtime - this.starttime) / (this.duration))
                tmpText = this.text[this.currline][0:numLetters]

            #first, render any finished lines
            for idx in range(this.currline):
                textSurface = this.font.render(this.text[idx], 0, colors.green_fg)
                if this.drawBackground:
                    backSurface = pygame.Surface(textSurface.get_size())
                    backSurface.fill(colors.green_bg)
                    screen.blit(backSurface, ( x, y + (idx * (this.fontSize + 3)))) #clear old pos
                screen.blit(textSurface, (x,y + (idx * (this.fontSize+3))))
            #finally, render the active line
            if (this.currline is not 1 or currtime > this.starttime):
                tmpText += "_"
                textSurface = this.font.render(tmpText, 0, colors.green_fg)
                if this.drawBackground:
                    backSurface = pygame.Surface(textSurface.get_size())
                    backSurface.fill(colors.green_bg)
                    screen.blit(backSurface, ( x, y + (this.currline * (this.fontSize + 3)))) #clear old pos
                screen.blit(textSurface, (x,y + (this.currline * (this.fontSize+3))))

            if (this.starttime != 0):
                if this.delayAtEndOfLine:
                    if (currtime > (this.starttime + this.duration + this.delay)):
                        this.currline += 1
                        this.starttime = pygame.time.get_ticks() + this.delay
                else:
                    if ( ( (currtime > (this.starttime + this.duration)) and (this.currline is not 1) ) or ( (currtime > (this.starttime + this.duration)) and (this.currline is 1) )):
                        this.currline += 1
                        this.starttime = currtime

        else:
            #animation is done, just show the lines
            for idx in range(len(this.text)):
                textSurface = this.font.render(this.text[idx], 0, colors.green_fg)

                if this.drawBackground:
                    backSurface = pygame.Surface(textSurface.get_size())
                    backSurface.fill(colors.green_bg)
                    screen.blit(backSurface, ( x, y + (idx * (this.fontSize + 3)))) #clear old pos

                screen.blit(textSurface, (x,y + (idx * (this.fontSize+3))))


class TypewriterCode:
    numLines = 0
    fontSize = 0

    def __init__(this, numLines, fontSize, maxLineLen=70, msPerChar=600):
        this.numLines = numLines
        this.fontSize = fontSize
        this.textQueue = collections.deque(maxlen=numLines)
        this.msPerChar = msPerChar
        this.nextCharTime = pygame.time.get_ticks() + msPerChar
        this.lineSpacing = 2
        this.maxLineLen = maxLineLen
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
        
class MumboText:
    def __init__(this, numLines, fontSize, msPerChar=200):
        this.numLines = numLines
        this.fontSize = fontSize
        this.textQueue = collections.deque(maxlen=numLines)
        this.msPerChar = msPerChar
        this.nextCharTime = pygame.time.get_ticks() + msPerChar
        this.lineSpacing = 2
        this.font=fonts.get(fontSize)
        this.fontSize = int(fontSize)
        if this.font is None:
            this.font = fonts.get('24')
            this.fontSize = 24
        this.textOptions = ["Collecting Garbage...OK", "Testing...OK", "Copy Auxiliary EXE...OK", "Align Microchips...OK",
        "Calculating Form Factor...OK", "Initiate Cross-Platform Play...OK", "COM Array Init...OK", "Calibrate VR Nodes...OK",
        "Service Satellite Oil...OK", "Increasing Bandwidth...OK", "Init Feed Transcoder...OK", "Sparking Chaos Drive...OK",
        "Depleting Uranium...OK", "Enable Neutral IR Inducer...OK", "Launching Steam...OK", "Ordering from Amazon...OK", 
        "Bracing for Warp...OK", "Waking Cryogenic Demons...OK", "Planning Family Outing...OK", "Bridging Bipolar Calibrator...OK",
        "Refresh Celeron Drive...OK", "Restricting Wide-Band Data...OK", "Bypass Cosmic Cluster...OK", "Decaying Isotopes...OK",
        "Polarizing Emergency Exits...OK", "Notifying Bridge Crew...OK", "Purchasing Enterprise Edition...OK", "Investing in Bitcoin...OK",
        "Connect to Central Server...OK", "Initializing Gray Protocol...OK", "Spoofing JPEGs...OK", "Mining Bitcoin...OK", "Building Usermap...OK",
        "Arming Satellite Cluster...OK", "Contacting Edge Nodes...OK", "Updating Utilities...OK", "Spawning Batch Jobs...OK",
        "Preparing Celebratory Fireworks...OK", "Aligning Satellite Constellation...OK", "Firing Thrusters...OK", 
        "Checking Network Interfaces...OK", "Baking Cakes...OK", "Earning Online Degree...OK", "Aligning Checksums...OK", "Enhancing Pixels...OK",
        "Downloading Firewall...OK", "Accessing Secure Network...OK", "Deploying Redshirts...OK", "Degrading Infrastructure...OK",
        "Rotating Anode...OK", "Splicing Neurons...OK", "Contesting Parking Fines...OK", "Encrypting Packets...OK", "Preparing Amino Chains...OK",
        "Starting Skyrim...OK", "Subscribing to Streaming Service...OK", "Moving Portable Quarry...OK", "Unit Testing...Error"]
    

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
            screen.blit(textSurface, ( x, y + (  (idx) * (this.lineSpacing + this.fontSize)) )) #fill new pos
        
        if len(this.textQueue) == this.numLines:
            this.textQueue.clear()
            this.nextCharTime = pygame.time.get_ticks() + (this.msPerChar*2)

        if pygame.time.get_ticks() > this.nextCharTime:
            this.nextCharTime = pygame.time.get_ticks() + this.msPerChar
            newLine = ""
            newLine = random.choice(this.textOptions)
            this.textQueue.append(newLine)

class TerminalText:
    def __init__(this, numLines, fontSize, msPerChar=200):
        this.numLines = numLines
        this.fontSize = fontSize
        this.textQueue = collections.deque(maxlen=numLines)
        this.msPerChar = msPerChar
        this.nextCharTime = pygame.time.get_ticks() + msPerChar
        this.lineSpacing = 2
        this.font=fonts.get(fontSize)
        this.fontSize = int(fontSize)
        if this.font is None:
            this.font = fonts.get('24')
            this.fontSize = 24

    def addLine(this, line):
        this.textQueue.appendleft(line)

    def clear(this):
        this.textQueue.clear()

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

