import ST7735S, time
from PIL import Image

screen = ST7735S.ST7735S()


img = Image.open("assets/space_test.jpg")
img2 = Image.open("assets/space_test_bubble.jpg")

while True:
	print("== Cycle")
	screen.draw(img)
	screen.draw(img2)

screen.close()