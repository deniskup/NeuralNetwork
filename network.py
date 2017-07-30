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
layers=3 #int(raw_input("Nombre de couches internes ? ")) # number of intermediate layers
inter=7 #int(raw_input("Neurones dans la couche intermediaire ? ")) # number of neurons on the intermediate layer (5 OK)
outputs=3



#number of backpropagations (100 000 OK)
nrand=100000 #int(raw_input("Nombres de pixels pour l'entrainement ? "))

#three dimensional array: weight[i][j][k] is the weight of layer i, from neuron j to neuron k
# i can go from 0 to inter
weight=[] 


#values of the neurons
#double dimension list: 0 is the input layer, 1 to layers is intermediate, layers+1 is the output layer
values=[[None]*inputs] # placeholders for inputs
for lay in range(layers):
	values.append([None]*inter) #intermediate layers
values.append([None]*outputs) #outputs

#learning rate (1 OK)
rate=1 #float(raw_input("Vitesse d'apprentissage ? "))


#number of inputs and outputs for a layer
def inout(lay):
	inp=inputs
 	if (lay>0):
 		inp=inter
 	out=inter
 	if(lay==layers):
 		out=outputs
 	return inp,out

#choose all weight randomly

for lay in range(layers+1):
	inp,out=inout(lay)
	weight.append([])
 	for i in range(inp):
 		weight[lay].append([])
 		for j in range(out):
 			weight[lay][i].append(random())

 	
#activation function: sigmoid
def activ(x):
	return 1/(1+exp(-x))


#load image to obtain size
fichier="colors.jpg" #raw_input("Fichier image a ouvrir ? ")
im=Image.open(fichier)
(width,height)=im.size
pixin=im.load()




#run the neural network on inputs [x,y], updates values of the network,
# result stored in outvalues, not normalized
def run(x,y):
	#normalize the input to values between -1 and 1
	normx=x/(width*1.0)-.5
	normy=y/(height*1.0)-.5
	values[0]=[normx,normy] #charging the inputs
	#compute values of intermediate neurons
	for lay in range(layers+1):
		inp,out=inout(lay)
		for j in range(out):
			val=0.
			for i in range(inp):
				val+=values[lay][i]*weight[lay][i][j]
			#apply activation function
			val=activ(val)
			values[lay+1][j]=val


#get a color from the output of a network (between 0 and 1)
def getcol(x):
	return int(floor(x*256))

#normalize a color from 0 to 255 to number between 0 and 1
def normcol(c):
	return c/(256*1.)
	
#get the color computed by the network
def result():
	colors=map(getcol,tuple(values[layers+1]))
	return tuple(colors)

#delta functions for backpropagation, from wikipedia

#i is the number of the output neuron, target the wanted value
def delta_output(i, target):
	val=values[layers+1][i]
	return (val-target)*val*(1-val)

#i is the number of the inner neuron, 
#delta_next the computed deltas for the next layer
def delta_mid(lay,i, delta_next):
	val=values[lay][i]
	s=0.
	for j in range(len(delta_next)):
		s+= delta_next[j]*weight[lay][i][j]
	return s*val*(1-val)


#backpropagation algorithm,
def backprop(x,y):
	run(x,y) #puts the right values of the neurons, by forward propagation
	#normalization of the colors to target values
	targets=map(normcol,pixin[x,y])
	#compute the deltas, starting from the output
	delta_out=[]
	for i in range(outputs):
		delta_out.append(delta_output(i,targets[i]))
	#delta_out is the current "next layer delta"

	delta_next=delta_out
	for lay in reversed(range(1,layers+1)):
	#back propagation of the deltas
		inp,out=inout(lay) #inp should always be inter here
		delta=[]
		for i in range(inter):
			delta.append(delta_mid(lay,i,delta_next))
		#changing the weight, using the formula w-= rate*o_i*delta_j
		for j in range(out):
			for i in range(inter):
				weight[lay][i][j]-= rate*values[lay][i]*delta_next[j]
		#storing the computed vector delta in delta_next for next step of backpropagation
		del delta_next[:]
		for i in range(inter):	
			delta_next.append(delta[i])
	#finally update first layer of weights
	for j in range(inter):
		for i in range(inputs):
			weight[0][i][j]-= rate*values[0][i]*delta_next[j]		





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


