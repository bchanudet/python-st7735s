import st7735s as controller
import time
from PIL import Image

screen = controller.ST7735S()

iterations = range(0, 255, 10)

#start = time.perf_counter() # Python 3
start = time.time()          # Python 2

for i in reversed(iterations):
     screen.fill([i, i, i])

for i in iterations:
     screen.fill([i, i, i])

#timeTaken = time.perf_counter() - start
timeTaken = time.time() - start
fps = 2 * len(iterations)/timeTaken

print("Time taken: {0:f}s".format(timeTaken))
print("Average FPS: {0:f}".format(fps))

screen.close()
