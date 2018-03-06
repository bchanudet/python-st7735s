import ST7735S, time
from PIL import Image

screen = ST7735S.ST7735S()

print("== COLOR")
screen.fill((0,255,0))

time.sleep(1)
print("")
print("== IMAGE")
img = Image.open("assets/galaxy.png")
screen.draw(img)
print("")

#screen.close()