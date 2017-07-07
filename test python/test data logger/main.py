#-*- coding: utf-8 -*-

import serial

buff = 0


arduino = serial.Serial('COM13', 9600, timeout=1)
fichier = open("data.txt", "a")

while 1:
	buff = arduino.readline()
	print(buff)
	fichier.write(buff)