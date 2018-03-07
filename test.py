import ST7735S, time
from PIL import Image

screen = ST7735S.ST7735S()

print("== COLOR")
start = time.perf_counter()

for i in range(25):
    screen.fill((0,255,0))
    screen.fill((255,0,0))
    screen.fill((0,0,255))

print("end", time.perf_counter() - start)    
