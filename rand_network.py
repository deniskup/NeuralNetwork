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

#values of the neurons
invalues=[0,0]
intervalues=[]
outvalues=[]

#learning rate
rate=.1


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

#derivative of the sigmoid
def deriv(x):
	return activ(x)*(1-activ(x))

#load image to obtain size
im = Image.open("imageGO.jpg")
(width,height)=im.size
pixin=im.load()

#run the neural network on inputs [x,y]
def run(x,y):
	#normalize the input to values between 0 and 1
	normx=x/(width*1.0)
	normy=y/(height*1.0)
	invalues[0]=normx
	invalues[1]=normy
	#compute values of intermediate neurons
	del intervalues[:]
	for j in range(inter):
		val=0.
		for i in range(inputs):
			val+=invalues[i]*weight1[i][j]
		#apply activation function
		val=activ(val)
		intervalues.append(val)
	#now compute output values
	del outvalues[:]
	for j in range(outputs):
		val=0.
		for i in range(inter):
			val+=intervalues[i]*weight2[i][j]
		#apply activation function
		val=activ(val)
		#scaling to obtain an integer between 0 and 255
		color=int(floor(val*256))
		outvalues.append(color)
		
	#return the RGB triplet
	return (outvalues[0],outvalues[1],outvalues[2])


#delta functions for backpropagation, from wikipedia

#i is the number of the output neuron, target the wanted value
def delta_output(i, target):
	val=outvalues[i]
	return (val-target)*val*(1-val)

#i is the number of the inner neuron, 
#deltas the computed deltas for the next layer

def delta_mid(i, deltas):
	val=intervalues[i]
	s=0
	for j in range(len(deltas)):
		s+= deltas[j]*weight2[i][j]
	return s*val*(1-val)

#backpropagation algorithm
def backprop(x,y):
	run(x,y) #puts the right values of the neurons
	tr,tg,tb= pixin[x,y] #pixel of the target image
	targets=[tr,tg,tb]
	#compute the deltas
	delta_out=[]
	for i in range(outputs):
		delta_out.append(delta_output(i,targets[i]))
	delta_inter=[]
	for i in range(inter):
		delta_inter.append(delta_mid(i,delta_out))
	#changing the weights
	#using the formula w-= rate*o_i*delta_j
	for j in range(outputs):
		for i in range(inter):
			weight2[i][j]-= rate*intervalues[i]*delta_out[j]
	for j in range(inter):
		for i in range(inputs):
			weight1[i][j]-= rate*invalues[i]*delta_inter[j]		



#number of backpropagations
nback=10

#do a round of backprops, one for each coordinate
def backprops():
	for x in range(width):
		for y in range(height):
			backprop(x,y)

for i in range(nback):
	backprops()

res=Image.new("RGB",(width,height))
pixout=res.load()
for x in range(width):
	for y in range(height):
		pixout[x,y]=run(x,y)

res.show()


