import copy
import math
import time

from PIL import Image

import RPi.GPIO as GPIO
import spidev


class Commands:
    SWRESET = 0x01
    SLPIN = 0x10
    SLPOUT = 0x11
    PTLON = 0x12
    NORON = 0x13
    INVOFF = 0x20
    INVON = 0x21
    DISPOFF = 0x28
    DISPON = 0x29
    CASET = 0x2A
    RASET = 0x2B
    RAMWR = 0x2C
    RAMRD = 0x2E
    PTLAR = 0x30
    MADCTL = 0x36
    COLMOD = 0x3A
    FRMCT1 = 0xB1
    FRMCT2 = 0xB2
    FRMCT3 = 0xB3
    INVCTR = 0xB4
    DISSET = 0xB6
    PWRCT1 = 0xC0
    PWRCT2 = 0xC1
    PWRCT3 = 0xC2
    PWRCT4 = 0xC3
    PWRCT5 = 0xC4
    VMCTR1 = 0xC5
    PWRCT6 = 0xFC
    GAMCTP = 0xE0
    GAMCTN = 0xE1


class ST7735S(object):

    def __init__(self):
        self.displayWidth = 132
        self.displayHeight = 162
        self.screenWidth = 128
        self.screenHeight = 128

        self.DC = 22
        self.Light = 18
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.DC, GPIO.OUT)
        GPIO.setup(self.Light, GPIO.OUT)

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 0x00

        self.reset()

    ## BASE FUNCTIONS

    def sendByte(self, byte):
        self.sendCommand(Commands.RAMWR)
        GPIO.output(self.DC, 1)
        self.spi.writebytes([byte])

    def sendManyBytes(self, bytes):
        self.sendCommand(Commands.RAMWR)
        print(bytes)
        GPIO.output(self.DC, 1)
        self.spi.writebytes(bytes)

    def sendCommand(self, command, *bytes):
        GPIO.output(self.DC, 0)
        self.spi.writebytes([command])
        
        if len(bytes) > 0:
            GPIO.output(self.DC, 1)
            self.spi.writebytes(list(bytes))
        
    def reset(self):        
        GPIO.output(self.Light, 0)
        print("reset")
        self.sendCommand(Commands.SWRESET)
        time.sleep(0.3)
        self.sendCommand(Commands.SLPOUT)
        time.sleep(0.3)
        self.sendCommand(Commands.DISPOFF)
        time.sleep(0.3)
        self.sendCommand(Commands.COLMOD, 0x06)
        self.sendCommand(Commands.DISPON)
        GPIO.output(self.Light, 1)

    def close(self):
        self.spi.close()
        GPIO.cleanup()

    def setWindow(self, x0, y0, x1, y1):
        print("setting window from {},{} to {},{}".format(x0,y0,x1,y1))
        self.sendCommand(Commands.CASET, 0, (x0 & 0xff), 0, (x1 & 0xff))
        self.sendCommand(Commands.RASET, 0, (y0 & 0xff), 0, (y1 & 0xff))

    ## COLOR CONVERSION
    
    def colorTo18(self, color):
        return [((color[0] >> 2) << 2),((color[1] >> 2) << 2),((color[2] >> 2) << 2)]

    def colorTo16(self, color):
        return (((color[2] // 8) << 11) | ((color[1] // 4) << 5) | (color[0] // 8) >> 8) & 0xff
    

    ## DRAWING FUNCTIONS

    def fill(self, color):
        self.setWindow(0, 0, self.screenWidth, self.screenHeight)
        print(self.colorTo18(color))

        for y in range(self.screenHeight):
            self.sendManyBytes(self.colorTo18(color) * self.screenWidth)

    def draw(self, image):

        pixels = list(image.getdata())

        self.setWindow(0, 0, self.screenWidth, self.screenHeight)

        converted = []
        for i in range(self.screenWidth * self.screenHeight):
            converted += self.colorTo18(pixels[i])

        print("got {} pixels for {} lines".format(len(converted), len(converted) // (self.screenWidth*3)))

        self.sendCommand(Commands.RAMWR)
        GPIO.output(self.DC, 1)

        i = 0
        tmpbuffer = []
        while i < len(converted):
            if i % (self.screenWidth*3) == 0:
                if len(tmpbuffer) > 0:
                    #print("sending {0}".format(len(tmpbuffer)))
                    self.spi.writebytes(tmpbuffer)
                tmpbuffer = []
                
            tmpbuffer.append(converted[i])
            i += 1
        
        if len(tmpbuffer) > 0:
            self.spi.writebytes(tmpbuffer)
        

