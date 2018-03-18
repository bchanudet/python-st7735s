import st7735s as controller
import time
from PIL import Image

screen = controller.ST7735S()
start = time.perf_counter()

for i in range(10):
    screen.fill((0,255,0))
    screen.fill((255,0,0))
    screen.fill((0,0,255))
    screen.fill((255,0,255))
    screen.fill((255,255,0))

timeTaken =  time.perf_counter() - start
fps = 50/timeTaken

print("Time taken: {0:f}s".format(timeTaken))
print("Average FPS: {0:f}".format(fps))
