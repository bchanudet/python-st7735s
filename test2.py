import ST7735S, time
from PIL import Image

screen = ST7735S.ST7735S()


img = Image.open("assets/space1.bmp")
img2 = Image.open("assets/space_test_bubble.jpg")

while True:
	print("== Cycle")
	screen.draw(img)
	#time.sleep(1)
	screen.draw(img2)
	#time.sleep(1)

screen.close()