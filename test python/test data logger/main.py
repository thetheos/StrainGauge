#-*- coding: utf-8 -*-

import serial

import matplotlib.pyplot as plt
import numpy as np
from drawnow import *

plt.ion()

buff = 0
inputVal = ['0','0'] #obliger d'initialiser le tableau
inputValInt = []
inputValInt1= []

arduino = serial.Serial('COM4', 9600, timeout=1)
fichier = open('data.txt', 'wb')

def plotValues():
	plt.plot(inputValInt, inputValInt1, 'o-')
	plt.grid(True)
	plt.ylim(300,500)

	plt.show()
	


while 1:
	while arduino.inWaiting():
		buff = arduino.readline()
		print(buff.decode('utf-8'))
		#print(buff.split())
		inputVal = buff.split()
		inputValUtf = [inputVal[0].decode('utf-8'),inputVal[1].decode('utf-8')]
		#print(inputValUtf[0])
		#print(inputValUtf[1])

		try:
			inputValInt.append(int(inputValUtf[0]))
			inputValInt1.append(int(inputValUtf[1]))
			#print(inputValInt1)
		except:
			print("")

		drawnow(plotValues)
		fichier.write(buff)


	