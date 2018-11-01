import st7735s as controller
import time
from PIL import Image

screen = controller.ST7735S()

img1 = Image.open("assets/1.jpg")
img2 = Image.open("assets/2.png")
img3 = Image.open("assets/sky.bmp")
img4 = Image.open("assets/time.bmp")

size = 64, 64
img1.thumbnail(size, Image.ANTIALIAS)
img2.thumbnail(size, Image.ANTIALIAS)
img3.thumbnail(size, Image.ANTIALIAS)
img4.thumbnail(size, Image.ANTIALIAS)

class G():
    L_IMG     = [img1, img2, img3, img4]
    L_SIZE    = len(L_IMG)
    L_IDX     = 0
    BACKLIGHT = False

Gray64 = [64, 64, 64] # [] for Python 2; () for Python 3
screen.fill( Gray64 )

start = time.time()

for i in range(10):
    screen.draw_at( G.L_IMG[G.L_IDX], x=0, y=0 )
    G.L_IDX = (G.L_IDX + 1) % G.L_SIZE

    screen.draw_at( G.L_IMG[G.L_IDX], x=64, y=0 )
    G.L_IDX = (G.L_IDX + 1) % G.L_SIZE

    screen.draw_at( G.L_IMG[G.L_IDX], x=64, y=64 )
    G.L_IDX = (G.L_IDX + 1) % G.L_SIZE

    screen.draw_at( G.L_IMG[G.L_IDX], x=0, y=64 )
    G.L_IDX = (G.L_IDX + 1) % G.L_SIZE

    screen.draw_at( G.L_IMG[G.L_IDX], x=32, y=32 )
    G.L_IDX = (G.L_IDX + 1) % G.L_SIZE

timeTaken = time.time() - start
fps = 50/timeTaken

print("Time taken: {0:f}s".format(timeTaken))
print("Average images per second: {0:f}".format(fps))

time.sleep(1)
screen.fill( Gray64 )

screen.close()
