from setuptools import setup

setup(name='st7735s',
      version='0.1',
      description='A class to send an image to a display driven by a ST7735S controller',
      url='https://github.com/bchanudet/python-st7735s',
      author='Benjamin Chanudet',
      author_email='hello@benjaminchanudet.com',
      license='MIT',
      packages=['st7735s'],
      install_requires=[
          'Pillow',
          'spidev',
          'RPi.GPIO'
      ],
      zip_safe=False)