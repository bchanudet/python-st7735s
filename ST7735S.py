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
    CMTEST = 0xF0
    PWRDIS = 0xF6


class ST7735S(object):

    def __init__(self):
        self.displayWidth   = 132
        self.displayHeight  = 162
        self.screenWidth    = 128
        self.screenHeight   = 128

        self.PinDC          = 22
        self.PinLight       = 18
        self.PinReset       = 13
        
        self.bitsPerPixel   = 18

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.PinDC, GPIO.OUT)
        GPIO.setup(self.PinLight, GPIO.OUT)
        GPIO.setup(self.PinReset, GPIO.OUT)

        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 8500000
        self.spi.mode = 0x00

        self.hardReset()
        self.reset()

    ## BASE FUNCTIONS

    def sendByte(self, byte):
        self.sendCommand(Commands.RAMWR)
        GPIO.output(self.PinDC, 1)
        self.spi.writebytes([byte])

    def sendManyBytes(self, bytes):
        self.sendCommand(Commands.RAMWR)
        print(bytes)
        GPIO.output(self.PinDC, 1)
        self.spi.writebytes(bytes)

    def sendCommand(self, command, *bytes):
        print("cmd", "{0:X}".format(command), bytes)
        GPIO.output(self.PinDC, 0)
        self.spi.writebytes([command])

        if len(bytes) > 0:
            GPIO.output(self.PinDC, 1)
            self.spi.writebytes(list(bytes))

    def hardReset(self):
        print("hard_reset")
        GPIO.output(self.PinReset, 1)
        time.sleep(.2)
        GPIO.output(self.PinReset, 0)
        time.sleep(.2)
        GPIO.output(self.PinReset, 1)
        time.sleep(.5)
        
    def reset(self):        
        GPIO.output(self.PinLight, 0)
        print("reset")
        self.sendCommand(Commands.SWRESET)
        time.sleep(0.3)
        self.sendCommand(Commands.DISPOFF)
        time.sleep(0.3)

        # Framerate
        self.sendCommand(Commands.FRMCT1, 0x01, 0x2c, 0x2d)
        self.sendCommand(Commands.FRMCT2, 0x01, 0x2c, 0x2d)
        self.sendCommand(Commands.FRMCT3, 0x01, 0x2c, 0x2d, 0x01, 0x2c, 0x2d)
        
        # Inversion
        self.sendCommand(Commands.INVCTR, 0x07)

        # Power sequence
        self.sendCommand(Commands.PWRCT1, 0xA2, 0x02, 0x84)
        self.sendCommand(Commands.PWRCT2, 0xC5)
        self.sendCommand(Commands.PWRCT3, 0x0A, 0x00)
        self.sendCommand(Commands.PWRCT4, 0x8A, 0x2A)
        self.sendCommand(Commands.PWRCT5, 0x8A, 0xEE)

        # Vcom ?
        self.sendCommand(Commands.VMCTR1, 0x0E)

        # gamma sequence
        self.sendCommand(Commands.GAMCTP, 0x0f, 0x1a, 0x0f, 0x18, 0x2f, 0x28, 0x20, 0x22, 0x1f, 0x1b, 0x23, 0x37, 0x00, 0x07, 0x02, 0x10)
        self.sendCommand(Commands.GAMCTN, 0x0f, 0x1b, 0x0f, 0x17, 0x33, 0x2c, 0x29, 0x2e, 0x30, 0x30, 0x39, 0x3f, 0x00, 0x07, 0x03, 0x10)

        # test command
        self.sendCommand(Commands.CMTEST, 0x01)

        # disable power save
        self.sendCommand(Commands.PWRDIS, 0x00)

        # mode 262k
        if self.bitsPerPixel == 18:
            self.sendCommand(Commands.COLMOD, 0x06)
        else:
            self.sendCommand(Commands.COLMOD, 0x05)

        self.sendCommand(Commands.MADCTL, 104)

        self.sendCommand(Commands.SLPOUT)
        time.sleep(0.3)
        self.sendCommand(Commands.DISPON)
        GPIO.output(self.PinLight, 1)

    def close(self):
        self.spi.close()
        GPIO.cleanup()

    def setWindow(self, x0, y0, x1, y1):
        print("setting window from {},{} to {},{}".format(x0,y0,x1,y1))
        self.sendCommand(Commands.CASET, 0, (x0 & 0xff) +1, 0, (x1 & 0xff) +1)
        self.sendCommand(Commands.RASET, 0, (y0 & 0xff) +2, 0, (y1 & 0xff) +2)

    ## COLOR CONVERSION

    def convColor(self, color):
        if self.bitsPerPixel == 18:
            return self.colorTo18(color)
        else:
            return self.colorTo16(color)
    
    def colorTo18(self, color):
        newColor =  [((color[0] >> 2) << 2),((color[1] >> 2) << 2),((color[2] >> 2) << 2)]
        return newColor

    def colorTo16(self, color):
        newColor = ((color[0] >> 3) << 11)|((color[1] >> 2) << 5)|(color[2] >> 3)
        return [newColor >> 8, newColor & 0xff]
    

    ## DRAWING FUNCTIONS

    def fill(self, color):
        self.setWindow(0, 0, self.displayWidth-1, self.displayHeight-1)

        converted = self.convColor(color)

        oneLine = converted * (self.displayWidth)
        print(oneLine)

        self.sendCommand(Commands.RAMWR)
        GPIO.output(self.PinDC, 1)

        for y in range(self.screenHeight):
            self.spi.writebytes(oneLine)

    def draw(self, image):

        pixels = list(image.getdata())

        self.setWindow(0, 0, self.screenWidth-1, self.screenHeight-1)

        converted = []
        for i in range(self.screenWidth * self.screenHeight):
            converted += self.convColor(pixels[i])

        bytePerPixel = 2
        if self.bitsPerPixel == 18 :
            bytePerPixel = 3

        print("got {} pixels for {} lines".format(len(converted), len(converted) // (self.screenWidth*bytePerPixel)))

        self.sendCommand(Commands.RAMWR)
        GPIO.output(self.PinDC, 1)

        i = 0
        tmpbuffer = []
        while i < len(converted):
            if i % (self.screenWidth*bytePerPixel*4) == 0:
                if len(tmpbuffer) > 0:
                    print("sending {0}".format(len(tmpbuffer)))
                    self.spi.writebytes(tmpbuffer)
                tmpbuffer = []
                
            tmpbuffer.append(converted[i])
            i += 1
        
        if len(tmpbuffer) > 0:
            self.spi.writebytes(tmpbuffer)
        

