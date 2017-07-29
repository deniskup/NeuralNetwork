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
layers=int(raw_input("Nombre de couches ? ")) # number of intermediate layers
inter=int(raw_input("Neurones dans la couche intermediaire ? ")) # number of neurons on the intermediate layer (5 OK)
outputs=3



#number of backpropagations (100 000 OK)
nrand=int(raw_input("Nombres de pixels pour l'entrainement ? "))

#three dimensional array: weight[i][j][k] is the weight of layer i, from neuron j to neuron k
# i can go from 0 to inter
weights=[] 


#values of the neurons
#double dimension list: 0 is the input layer, 1 to inter is intermediate, inter+1 is the output layer
values=[[None,None]] # placeholders for inputs
for lay in range(layers):
	values.append([None]*inter) #intermediate layers
values.append([None,None,None]) #outputs

#learning rate (1 OK)
rate=float(raw_input("Vitesse d'apprentissage ? "))


#number of inputs and outputs for a layer
def inout(lay):
	inp=inputs
 	if (lay>0):
 		inp=inter
 	out=inter
 	if(lay==layers):
 		out=outputs
 	return inp,out

#choose all weights randomly
#first weight1
for lay in range(layers+1):
	inp,out=inout(lay)
	wlay=[]
 	for i in range(inp):
 		wi=[]
 		for j in range(out):
 			wi.append(random())
 		wlay.append(wi)
 	weights.append(wlay)
 	
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
	values[0]=[normx,normy]) #changing the inputs
	#compute values of intermediate neurons
	for lay in range(layers+1):
		inp,out=inout(lay)
		for j in range(out):
			val=0.
			for i in range(inp):
				val+=values[l][i]*weight[l][i][j]
			#apply activation function
			val=activ(val)
			values[l+1][j]=val

#get the color computed by the network
def result():
	colors=map(getcol,tuple(outvalues))
	return tuple(colors)

#delta functions for backpropagation, from wikipedia

#i is the number of the output neuron, target the wanted value
def delta_output(i, target):
	val=values[layers+1][i]
	return (val-target)*val*(1-val)

#i is the number of the inner neuron, 
#deltas the computed deltas for the next layer

def delta_mid(lay,i, deltas):
	val=values[lay][i]
	s=0
	for j in range(len(deltas)):
		s+= deltas[j]*weight[lay][i][j]
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
	for lay in reversed(range(1,layers+1)):
	#todo from here: reverse loop doing back propagation
	##
	## below is incorrect, to be fixed
		inp,out=inout(lay)
		for i in range(inter):
			delta_inter.append(delta_mid(lay,i,delta_out))
		#changing the weights
		#using the formula w-= rate*o_i*delta_j
		for j in range(out):
			for i in range(inter):
				weight[lay][i][j]-= rate*intervalues[i]*delta_out[j]






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


