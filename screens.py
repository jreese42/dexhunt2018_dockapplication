from shapes import BorderRect
from shapes import SolidRect
from widgets import TextBox
from widgets import Meter
from widgets import TypewriterText
from widgets import TypewriterCode
from widgets import MumboText
from widgets import TerminalText

from random import randint

from networkmodel import DeviceModel
import colors
import pygame

class LoggedOutScreen:
    def __init__(self):
        self.borderRect = BorderRect(1280-60-60,720-60-60,1)
        self.typewriterText = TypewriterText()
        self.typewriterText.animateText("PLACE ARTIFACT IN DOCK", 1)
        self.footerText = TypewriterText(fontSize='16')
        self.footerText.animateText("USAF 00fb.0002.2311 74945fae569355c7", 0.5)
        self.tinytext = TypewriterText(fontSize='8')
        self.tinytext.animateText("Booting...OK\nConnect to Central Server...OK\nInitializing Gray Protocol...OK\nSpoofing JPEGs...OK\nMining Bitcoin...OK\nBuilding Usermap...OK\nArming Satellite Cluster...OK\nContacting Edge Nodes...OK\nUpdating Utilities...OK\nSpawning Batch Jobs...OK\nPreparing Celebratory Fireworks...OK\nAligning Satellite Constellation...OK\nFiring Thrusters...OK\nChecking Network Interfaces...OK\nBaking Cakes...OK\nEarning Online Degree...OK\nAligning Checksums...OK\nEnhancing Pixels...OK\nDownloading Firewall...OK\nAccessing Secure Network...OK\n\nBoot Sequence Complete\n\nVERSION 005b68d\nSystem Loaded in 30.2238s\n\nInitializing Hardware\nReady for Hardware Interface\nOK", 0.25)
    
    def draw(self,surface):
        self.typewriterText.draw(surface,160,160)
        self.footerText.draw(surface, 920,665)
        self.tinytext.draw(surface,1040,310)
        self.borderRect.draw(surface,60,60)

class LoggingInTransitionScreen:
    def __init__(self):
        self.borderRect = BorderRect(1280-60-60,720-60-60,1)
        self.footerText = TypewriterText(fontSize='16')
        self.footerText.animateText("USAF 00fb.0002.2311 74945fae569355c7", 0.5)
        self.tinytext = TypewriterText(fontSize='10')
        self.tinytext.animateText("Booting...OK\nConnect to Central Server...OK\nInitializing Gray Protocol...OK\nSpoofing JPEGs...OK\nMining Bitcoin...OK\nBuilding Usermap...OK\nArming Satellite Cluster...OK\nContacting Edge Nodes...OK\nUpdating Utilities...OK\nSpawning Batch Jobs...OK\nPreparing Celebratory Fireworks...OK\nAligning Satellite Constellation...OK\nFiring Thrusters...OK\nChecking Network Interfaces...OK\nBaking Cakes...OK\nEarning Online Degree...OK\nAligning Checksums...OK\nEnhancing Pixels...OK\nDownloading Firewall...OK\nAccessing Secure Network...OK\n\nBoot Sequence Complete\n\nVERSION 005b68d\nSystem Loaded in 30.2238s\n\nInitializing Hardware\nReady for Hardware Interface\nOK", 0.025)
    
    def resetAnimation(self):
        self.footerText = TypewriterText(fontSize='16')
        self.footerText.animateText("USAF 00fb.0002.2311 74945fae569355c7", 0.5)
        self.tinytext = TypewriterText(fontSize='10')
        self.tinytext.animateText("Booting...OK\nConnect to Central Server...OK\nInitializing Gray Protocol...OK\nSpoofing JPEGs...OK\nMining Bitcoin...OK\nBuilding Usermap...OK\nArming Satellite Cluster...OK\nContacting Edge Nodes...OK\nUpdating Utilities...OK\nSpawning Batch Jobs...OK\nPreparing Celebratory Fireworks...OK\nAligning Satellite Constellation...OK\nFiring Thrusters...OK\nChecking Network Interfaces...OK\nBaking Cakes...OK\nEarning Online Degree...OK\nAligning Checksums...OK\nEnhancing Pixels...OK\nDownloading Firewall...OK\nAccessing Secure Network...OK\n\nBoot Sequence Complete\n\nVERSION 005b68d\nSystem Loaded in 30.2238s\n\nInitializing Hardware\nReady for Hardware Interface\nOK", 0.01)

    def draw(self,surface):
        self.footerText.draw(surface, 920,665)
        self.tinytext.draw(surface,560,150)
        self.borderRect.draw(surface,60,60)

class LoggedInScreen:
    def __init__(self):
        self.borderRect = BorderRect(1160,600,1)

        self.meters = []
        self.meterChangePeriod = 3000
        self.meterChangeTime = pygame.time.get_ticks() + self.meterChangePeriod
        for idx in range(5):
            self.meters.append(Meter(50, 200, 10, 10, thiccness=1))
            self.meters[idx].setValue(randint(0, 10))

        self.inputPasswordText = TypewriterText()
        self.inputPasswordText.animateText("INPUT PASSWORD", 1)

        self.typewriterCode = TypewriterCode(numLines=49, fontSize=10, msPerChar=30, maxLineLen=50)

        self.textBox = TextBox(maxlen=20)
        self.textboxRect = BorderRect(400, 150, 2)

        self.footerText = TypewriterText(fontSize='16')
        self.footerText.animateText("USAF 00fb.0002.2311 74945fae569355c7", 0.5)

        self.mumbotext = MumboText(20, '12')

        self.statusText = TerminalText(numLines=16, fontSize='16')
        self.statusRect = BorderRect(400, 300, 2)

    def reset(self):
        self.statusText.clear()
    
    def draw(self,surface):
        textBoxRootX = 440
        textBoxRootY = 440

        self.borderRect.draw(surface,60,60)
        for idx,meter in enumerate(self.meters):
            meter.draw(surface,80+idx*60, 80)
        self.typewriterCode.draw(surface,930,640)
        self.footerText.draw(surface, 920,665)
        self.mumbotext.draw(surface, 80, 310)

        self.textboxRect.draw(surface, textBoxRootX, textBoxRootX)
        self.inputPasswordText.draw(surface, textBoxRootX + 10, textBoxRootY + 10)
        self.textBox.draw(surface,textBoxRootX + 55, textBoxRootY + 85)
        self.statusRect.draw(surface, textBoxRootX, textBoxRootY - 310)
        self.statusText.draw(surface, textBoxRootX + 10, textBoxRootY - 32)

        if pygame.time.get_ticks() > self.meterChangeTime:
            self.meterChangeTime = pygame.time.get_ticks() + self.meterChangePeriod
            for idx in range(5):
                self.meters[idx].setValue(randint(2, 10))
    
    def sendKeyToTextBox(self, key):
        text = self.textBox.getText() + str(key)
        self.textBox.setText(text)

    def clearTextBox(self):
        self.textBox.setText("")
    
    def textBoxBackspace(self):
        text = self.textBox.getText()[:-1]
        self.textBox.setText(text)

    def getPassword(self):
        return self.textBox.getText()

    def sendLineToTerminal(self, line):
        self.statusText.addLine(line)
