#-*- coding: utf-8 -*-

import serial

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib import style
import time

buff = 0
inputVal = ['100','100'] #obliger d'initialiser le tableau
inputValInt = [0]
inputValInt1= [0]
aquisitionTime= 10000 #ddefault 1000, 
arduino = serial.Serial('COM4', 9600, timeout=1)
fileName = time.strftime("%Y-%m-%d_%H-%M-%S")
fichier = open('data'+fileName+ '.txt', 'wb')


style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
	ax1.clear()
	ax1.plot(inputValInt,inputValInt1)
	last = len(inputValInt)
	lastVal = inputValInt[last-1]
	ax1.set_xlim([0+lastVal-aquisitionTime	,lastVal]	) #comment for no x axis mouvement
	get_data()	
	
def get_data():
	while arduino.inWaiting():
		buff = arduino.readline()
		#print(buff.decode('utf-8'))
		#print(buff.split())
		inputVal = buff.split()
		#print(inputValUtf[0])
		#print(inputValUtf[1])
		try:
			inputValUtf = [inputVal[0].decode('utf-8'),inputVal[1].decode('utf-8')]
		except:
			print("")	

		try:
			inputValInt.append(int(inputValUtf[0]))
			inputValInt1.append(int(inputValUtf[1]))
		except:
			print("")

		fichier.write(buff)


while 1:	
	ani = animation.FuncAnimation(fig, animate, interval=10)
	
	plt.show()
	#print(inputValInt1)
		


