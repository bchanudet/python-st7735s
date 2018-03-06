import ST7735S, time
from PIL import Image

screen = ST7735S.ST7735S()

print("== COLOR")
screen.fill((255,0,0))

time.sleep(1)
print("")
print("== IMAGE")
img = Image.open("BACKGROUND.png")
screen.draw(img)
print("")

screen.close()