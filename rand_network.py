# toy neural network for image reproduction, for now just chosen at random


#import modules
from PIL import Image
from random import random


# 2 inputs for coordinates x,y
# 3 outputs for R,G,B
# one intermediate layer, here 5 neurons

inputs=2
inter=5 # number of neurons on the intermediate layer
outputs=3

weight1=[] #two-dimensional array for inputs to inter
weight2=[] #two-dimensional array for inter to output

#choose all weights randomly
#first weight1
for i in range(inputs):
 	wl=[]
 	for j in range(inter):
 		wl.append(random())
 	weight1.append(wl)
#then weight2
for i in range(inter):
 	wl=[]
 	for j in range(outputs):
 		wl.append(random())
 	weight2.append(wl)
 

def changepix(pix):
	return pix


im = Image.open("imageGO.jpg")
(width,height)=im.size
res=Image.new("RGB",(width,height));
pix1=im.load()
pix2=res.load()
for x in range(width):
	for y in range(height):
		pix2[x,y]=changepix(pix1[x,y])

res.show()


