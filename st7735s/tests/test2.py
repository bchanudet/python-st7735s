import st7735s as controller
import time
from PIL import Image

screen = controller.ST7735S()
start = time.perf_counter()

img = Image.open("assets/1.png")
img2 = Image.open("assets/2.png")

for i in range(10):
	screen.draw(img)
	screen.draw(img2)

timeTaken =  time.perf_counter() - start
fps = 20/timeTaken

print("end")
print("Time taken: {0:f}s".format(timeTaken))
print("Average FPS: {0:f}".format(fps))

screen.close()