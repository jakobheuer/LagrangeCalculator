import numpy as np
from PIL import Image
import math


au = 149597870700 #Astronomical unit [m]

#Resolution
imgRes = 250
imgResX = imgRes
imgResY = imgRes
scale = 3 * au #Total width of image
pixelDistanceMeters = scale / imgRes #1 Pixel is this much meters
pixelDistanceAu =  pixelDistanceMeters / au #1 Pixel is this much au

class Sun:
    mass = 1.989e30
    x = round(imgResX / 2)
    y = -round(imgResY / 2)
sun = Sun()

class Earth:
    mass = 5.972e24
    x = sun.x + round(au/pixelDistanceMeters)
    y = sun.y
    speed = 29722.2 #m/s
    angularVelocity = 2e-7
earth = Earth()

class Satellite:
    mass = 1000
sat = Satellite()

centrifugalForce = np.zeros( (imgResX,imgResY,3), dtype=np.float64)
conservationForce = np.zeros( (imgResX,imgResY,3), dtype=np.float64) #möglicherweiße nutzlos weil 0 da keine beschleunigung

data = np.zeros( (imgResX,imgResY,3), dtype=np.uint8 )

for x in range(imgResX):
    for y in range(imgResY):
        c = (math.sqrt(((abs(x - sun.x)) ** 2) + ((abs(y - sun.y)) ** 2))) * pixelDistanceMeters
        centrifugalForce[x,y,1] = -1*(sun.x - x)
        centrifugalForce[x, y, 2] = -1*(sun.y - -y)
        if x == sun.x and -y == sun.y: #would be infinit
            centrifugalForce[x,y,0] = 0
            conservationForce[x,y,0] = 0
            centrifugalForce[x, y, 1] = 0
            centrifugalForce[x, y, 1] = 0
        else:
            centrifugalForce[x,y,0] = earth.mass * (earth.speed/c)
            conservationForce[x, y,0] = sat.mass * (earth.angularVelocity)*c #F=m*a a=angular velocity * r
            #centrifugalForce[x, y, 1] = (1 / math.sqrt((centrifugalForce[x, y, 1] ** 2) + (centrifugalForce[x, y, 2] ** 2))) * centrifugalForce[x, y, 1]
            #centrifugalForce[x, y, 1] = (1 / math.sqrt((centrifugalForce[x, y, 1] ** 2) + (centrifugalForce[x, y, 2] ** 2))) * centrifugalForce[x, y, 2]

print(sun.x)
print(sun.y)
print(x)
print(y)
print(centrifugalForce[0,0])
print(centrifugalForce[249,0])
print(centrifugalForce[0,249])
print(centrifugalForce[249,249])
#Create Array
#data = np.zeros( (imgResX,imgResY,3), dtype=np.uint8 )

#for x in range(imgResX):
    #for y in range(imgResY):
        #c = data[x,y,0]
        #data[x,y] = [max*c,max*c,max*c]

#img = Image.fromarray( data )       # Create a PIL image
#img.show()                      # View in default viewer