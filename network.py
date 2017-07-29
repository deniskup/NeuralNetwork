# toy neural network for image reproduction, for now just chosen at random
#in this version several layers are possible (not done yet)

#import modules
from PIL import Image
from random import *
from math import *



#### parametres du reseau ###########

# 2 inputs for coordinates x,y
# 3 outputs for R,G,B
# one intermediate layer, here 5 neurons

inputs=2
inter=int(raw_input("Neurones dans la couche intermediaire ? ")) # number of neurons on the intermediate layer (5 OK)
outputs=3


#number of backpropagations (100 000 OK)
nrand=int(raw_input("Nombres de pixels pour l'entrainement ? "))

weight1=[] #two-dimensional array for inputs to inter
weight2=[] #two-dimensional array for inter to output

#values of the neurons
invalues=[0,0]
intervalues=[]
outvalues=[]

#learning rate (1 OK)
rate=float(raw_input("Vitesse d'apprentissage ? "))


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
fichier=raw_input("Fichier image a ouvrir ? ")
im=Image.open(fichier)
(width,height)=im.size
pixin=im.load()


#normalize a color from 0 to 255 to number between 0 and 1
def normcol(c):
	return c/(256*1.)
	
#get a color from the output of a network (between 0 and 1)
def getcol(x):
	return int(floor(x*256))

#run the neural network on inputs [x,y], updates values of the network,
# result stored in outvalues, not normalized
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
		outvalues.append(val)

#get the color computed by the network
def result():
	colors=map(getcol,tuple(outvalues))
	return tuple(colors)

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


#backpropagation algorithm,
def backprop(x,y):
	#print "frontprop"
	run(x,y) #puts the right values of the neurons, by forward propagation
	#print "backprop"
	tr,tg,tb= pixin[x,y] #pixel of the target image
	#normalization of the colors to target values
	targets=map(normcol,[tr,tg,tb])
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






print "random sampling..."
for i in range(nrand):
	x=randint(0,width-1)
	y=randint(0,height-1)
	backprop(x,y)

	
res=Image.new("RGB",(width,height))
pixout=res.load()
for x in range(width):
	for y in range(height):
		run(x,y)
		pixout[x,y]=result()
		#print pixout[x,y]

res.show()


