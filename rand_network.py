# toy neural network for image reproduction, for now just chosen at random


#import modules
from PIL import Image
from random import random
from math import *

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
 


#activation function
#let's try with the sigmoid
def activ(x):
	return 1/(1+exp(-x))

#run the neural network on inputs [x,y]
def run(inp):
	#compute values of intermediate neurons
	intvalues=[]
	for j in range(inter):
		val=0
		for i in range(inputs):
			val+=inp[i]*weight1[i][j]
		#apply activation function
		val=activ(val)
		intvalues.append(val)
	#now compute output values
	outvalues=[]
	for j in range(outputs):
		val=0
		for i in range(inter):
			val+=intvalues[i]*weight2[i][j]
		#apply activation function
		val=activ(val)
		#scaling to obtain an integer between 0 and 255
		color=int(val*256)
		outvalues.append(color)
		
	#return the RGB triplet
	print outvalues
	return (outvalues[0],outvalues[1],outvalues[2])


im = Image.open("imageGO.jpg")
(width,height)=im.size
res=Image.new("RGB",(width,height))
pix1=im.load()
pix2=res.load()
for x in range(width):
	for y in range(height):
		pix2[x,y]=run([x,y])

res.show()


