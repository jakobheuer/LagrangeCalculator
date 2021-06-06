import numpy as np
from PIL import Image
import math

imgResX = 255
imgResY = 255
max = 0
c = 0.0
middleX=imgResX / 2
middleY=imgResY / 2

data = np.zeros( (imgResX,imgResY,3), dtype=np.uint8 )

#data[512,512] = [254,0,0]       # Makes the middle pixel red
#data[512,513] = [0,0,255]       # Makes the next pixel blue

for x in range(imgResX):
    for y in range(imgResY):
        c = math.sqrt( ((abs(x-middleX))**2) + ((abs(y-middleY))**2) )
        data[x,y] = [c,0,0]

max = np.max(data)
max=255/max

for x in range(imgResX):
    for y in range(imgResY):
        c = data[x,y,0]
        data[x,y] = [max*c,max*c,max*c]

img = Image.fromarray( data )       # Create a PIL image
img.show()                      # View in default viewer