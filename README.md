# python-st7735s

This simple class allows you to send images to a LCD display driven by a ST7735S Controller, from a Raspbery Pi. 

The one I own and do tests on is the [128x128 1.44" HAT from Waveshare](https://www.waveshare.com/1.44inch-lcd-hat.htm). It is plugged on a Raspberry Pi Zero.

The code is compatible with Python 3.5 and up, and heavily inspired by [this repository](https://github.com/jackw01/raspi-python-st7735)  from @jackw01.

# Performances

On my Raspberry Pi Zero, the package reaches 5 FPS while doing refresh of the complete display. Performances should be better if I implement like a framebuffer and only update the modified pixels, but honestly 5FPS is all I need for now.

# Requirements

- `Pillow` : for handling image operations
- `spidev` : sending data via SPI
- `RPi.GPIO`  : handling gpios for sending commands

# Usage 

    >>> import st7735s as Controller
    >>> from PIL import Image
    >>> screen = Controller.ST7735S()
    >>> img = Image.open("assets/test.bmp")
    >>> screen.draw(img)

# Installation

```bash
$ git clone https://github.com/bchanudet/python-st7735s.git
$ cd python-st7735s
# choose one of these two commands:
$ python3 setup.py install -e . # install with a symlink, so you're one git fetch from the last version
$ python3 setup.py install .    # install globally without references to this folder.
``` 