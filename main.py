import numpy as np
from PIL import Image
import math


au = 149597870700 #Astronomical unit [m]
G = 6.67259e-11 #Gravitational constant

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
    #mass = 0.5e30
sat = Satellite()

centrifugalForce = np.zeros( (imgResX,imgResY,3), dtype=np.float64)
gravitationalForce = np.zeros( (imgResX,imgResY,3), dtype=np.float64)
totalForce = np.zeros( (imgResX,imgResY,3), dtype=np.float64)
data = np.zeros( (imgResX,imgResY,3), dtype=np.uint8 )

for x in range(imgResX):
    for y in range(imgResY):
        c = (math.sqrt(((abs(x - sun.x)) ** 2) + ((abs(y - -sun.y)) ** 2))) * pixelDistanceMeters
        centrifugalForce[x,y,1] = -1*(sun.x - x)
        centrifugalForce[x, y, 2] = -1*(sun.y - -y)
        gravitationalForce[x, y, 1] = (sun.x - x)
        gravitationalForce[x, y, 2] = (sun.y - -y)
        #print("X: " +str(x)+", Y: "+str(y))
        if x != sun.x or -y != sun.y: #would be infinite
            centrifugalForce[x, y, 0] = sat.mass * (((earth.angularVelocity*c)**2) / c)
            betrag = math.sqrt((centrifugalForce[x, y, 1] ** 2) + ((centrifugalForce[x, y, 2] ** 2)))
            centrifugalForce[x, y, 1] = (1 / betrag) * centrifugalForce[x, y, 1]  # X Normalisiert
            centrifugalForce[x, y, 2] = (1 / betrag) * centrifugalForce[x, y, 2]  # Y Normalisiert
            centrifugalForce[x, y, 1] = centrifugalForce[x,y,1] * centrifugalForce[x,y,0]
            centrifugalForce[x, y, 2] = centrifugalForce[x,y,2] * centrifugalForce[x,y,0]

            gravitationalForce[x, y, 0] = G * ((sun.mass * sat.mass) / (c ** 2))
            betrag = math.sqrt((gravitationalForce[x, y, 1] ** 2) + ((gravitationalForce[x, y, 2] ** 2)))
            gravitationalForce[x, y, 1] = (1 / betrag) * gravitationalForce[x, y, 1]  # X Normalisiert
            gravitationalForce[x, y, 2] = (1 / betrag) * gravitationalForce[x, y, 2]  # Y Normalisiert
            gravitationalForce[x, y, 1] = gravitationalForce[x,y,1] * gravitationalForce[x,y,0]
            gravitationalForce[x, y, 2] = gravitationalForce[x, y, 2] * gravitationalForce[x, y, 0]

            totalForce[x, y, 1] = gravitationalForce[x, y, 1] + centrifugalForce[x, y, 1]
            totalForce[x, y, 2] = gravitationalForce[x, y, 2] + centrifugalForce[x, y, 2]
            totalForce[x, y, 0] = math.sqrt((totalForce[x, y, 1]**2) + (totalForce[x, y, 2]**2))


max = np.max(gravitationalForce)
max=255/max

for x in range(imgResX):
    for y in range(imgResY):
        c = gravitationalForce[x, y, 0]
        #d = gravitationalForce[x, y, 1]
        #e = gravitationalForce[x, y, 2]
        data[x, y] = [max * c, 0, 0]
img = Image.fromarray( data )       # Create a PIL image
img.show()                      #View in default viewer


max = np.max(centrifugalForce)
max=255/max

for x in range(imgResX):
    for y in range(imgResY):
        c = centrifugalForce[x, y, 0]
        #d = centrifugalForce[x, y, 1]
        #e = centrifugalForce[x, y, 2]
        data[x, y] = [max * c, 0, 0]
img = Image.fromarray( data )       # Create a PIL image
img.show()     # View in default viewer

max = np.max(totalForce)
max=255/max

for x in range(imgResX):
    for y in range(imgResY):
        c = totalForce[x, y, 0]
        #d = totalForce[x, y, 1]
        #e = totalForce[x, y, 2]
        data[x, y] = [max * c, 0, 0]
        if x == earth.x and -y == earth.y:
            data[x, y] = [255, 255, 255]
            print(earth.y)
            print(earth.x)
            print(x)
            print(y)
data[20, 0] = [255, 255, 0]
img = Image.fromarray( data )       # Create a PIL image
img.show()                      # View in default viewer

#print(sun.y)
#print(sun.x)
#print(x)
#print(y)
#print(centrifugalForce[0,0])
#print(centrifugalForce[125,125])
#print(centrifugalForce[249,0])
#print(centrifugalForce[0,249])
#print(centrifugalForce[249,249])
#print(gravitationalForce[0,0])
#print(gravitationalForce[123,123])
#print("Total:")
#print(totalForce[0,0])
#print(totalForce[0,249])
#print(totalForce[249,249])

#Create Array
#data = np.zeros( (imgResX,imgResY,3), dtype=np.uint8 )

#for x in range(imgResX):
    #for y in range(imgResY):
        #c = data[x,y,0]
        #data[x,y] = [max*c,max*c,max*c]

# img = Image.fromarray( data )       # Create a PIL image
# img.show()                      # View in default viewer