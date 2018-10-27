import st7735s as controller
import time
from PIL import Image

screen = controller.ST7735S()

colors = []

# Tested with Python 2.7, so color is list (tuple for Python 3)
colors.append([0, 0, 0]) # black
colors.append([48, 48, 48]) # Gray
colors.append([64, 64, 64])
colors.append([128, 128, 128])
colors.append([164, 164, 164])
colors.append([192, 192, 192])
colors.append([208, 208, 208])
colors.append([224, 224, 224])
colors.append([255, 255, 255]) # White
colors.append([255, 0, 0]) # Red
colors.append([255, 64, 0]) # Orange
colors.append([255, 208, 0]) # Yellow
colors.append([0, 255, 0]) # Green
colors.append([0, 255, 128]) # Teal
colors.append([0, 128, 255]) # LightBlue
colors.append([0, 64, 255])  # Blue
colors.append([144, 0, 255]) # Purple
colors.append([255, 0, 255]) # Magenta

SEC = 0.8

for c in colors:
    screen.fill(c)
    time.sleep(SEC)

screen.close()
