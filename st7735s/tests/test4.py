import st7735s as controller
import time
from PIL import Image

screen = controller.ST7735S()

img = Image.open("assets/sky.bmp")
img2 = Image.open("assets/time.bmp")

#start = time.perf_counter() # Python 3
start = time.time()          # Python 2

for i in range(10):
    screen.draw_at(img)
    screen.draw_at(img2)

#timeTaken =  time.perf_counter() - start
timeTaken = time.time() - start
fps = 20/timeTaken

print("Time taken: {0:f}s".format(timeTaken))
print("Average FPS: {0:f}".format(fps))

screen.close()
