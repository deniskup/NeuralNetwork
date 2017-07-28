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
 		wl.append(random()*10-5)
 	weight1.append(wl)
#then weight2
for i in range(inter):
 	wl=[]
 	for j in range(outputs):
 		wl.append(random()*10-5)
 	weight2.append(wl)
 


#activation functions
#identity
def activid(x):
	return x

#sigmoid
def activ(x):
	return 1/(1+exp(-x))


#load image to obtain size
im = Image.open("imageGO.jpg")
(width,height)=im.size
pixin=im.load()

#run the neural network on inputs [x,y]
def run(inp):
	#normalize the input to values between 0 and 1
	normx=inp[0]/(width*1.0)
	normy=inp[1]/(height*1.0)
	inval=[normx,normy]
	#compute values of intermediate neurons
	intvalues=[]
	for j in range(inter):
		val=0.
		for i in range(inputs):
			val+=inval[i]*weight1[i][j]
		#apply activation function
		val=activ(val)
		intvalues.append(val)
	#now compute output values
	outvalues=[]
	for j in range(outputs):
		val=0.
		for i in range(inter):
			val+=intvalues[i]*weight2[i][j]
		#apply activation function
		val=activ(val)
		#scaling to obtain an integer between 0 and 255
		color=int(floor(val*256))
		outvalues.append(color)
		
	#return the RGB triplet
	#print outvalues
	return (outvalues[0],outvalues[1],outvalues[2])



res=Image.new("RGB",(width,height))
pixout=res.load()
for x in range(width):
	for y in range(height):
		pixout[x,y]=run([x,y])

res.show()


