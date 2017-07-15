#!/usr/bin/env python
# a bar plot with errorbars
#-*- coding: utf-8 -*-
import serial
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
import kivy.uix.layout 
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial
from kivy.uix.widget import Widget
#matplotlib.use('Gtk')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '1900')
Config.set('graphics', 'height', '1000')
Config.set('graphics', 'resizable','1')
Config.write()
import sys
import glob

buff = 0
inputVal = ['100','100'] #obliger d'initialiser le tableau
inputValInt = [0,10]
inputValInt1= [0,10]
inputValUtf = [0,0]
aquisitionTime= 1000 #ddefault 1000, 
inputMaxVal = 0
inputMaxValStr = "max: NaN"
i= True




            


        

class MyApp(App):
    def callback(self,instance):
        self.beginSerial()

    def callback1(self, instance):
        self.clearData()

    def build(self):
        self.buildPlot()
        fileName = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.fichier = open('data'+fileName+ '.txt', 'wb')
        self.box = FloatLayout(size = (300,300))



        self.plotter = FigureCanvasKivyAgg(plt.gcf(), size_hint = (0.75,0.6), pos_hint ={'center_x':.5, 'top':1})
        self.button = Button(text="Begin Serial", font_size=14,size_hint = (.1,.1), pos_hint = {'left':1, 'bottom':1})
        self.button.bind(on_press= self.callback)
        self.buttonWippeDate = Button(text = "wippe data", font_size=14, size_hint=(0.1,0.1), pos_hint = {'right':1, 'bottom':1})
        self.buttonWippeDate.bind(on_press=self.callback1)
        self.maxLabel= Label(text="max: NaN",font_size=48,pos_hint = {'center_x':.5, 'top':.8})
        self.serialInput = Label(text="Serial input:", font_size=48, pos_hint ={'center_x':.7,'top':.8})

        i =True
        self.box.add_widget(self.plotter)
        self.box.add_widget(self.button)
        self.box.add_widget(self.buttonWippeDate)
        self.box.add_widget(self.maxLabel)
        self.box.add_widget(self.serialInput)


        print("running")
        print(self.serial_ports())

        return self.box

    def beginSerial(self):
        global i
        if i:
            self.arduino = serial.Serial('COM4', 9600, timeout=1)
            self.updateAnimate = Clock.schedule_interval(self.animate,0)
            print("Serial connection error")
            print(i)
            self.button.text= "Stop serial"
            i = False
        else:
            self.clearData()
            Clock.unschedule(self.updateAnimate)
            self.arduino.close()
            print(i)
            self.button.text = "Begin serial"
            
            i= True

    def buildPlot(self):
        style.use('fivethirtyeight')
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.ax1.clear()
        self.ax1.plot(inputValInt,inputValInt1)

    def clearData(self):
        global inputMaxVal

        del inputValInt[:]
        del inputValInt1[:]
        inputMaxVal = 0
        self.maxLabel.text = "max: NaN"
        print("data wipped")


    def animate(self,dt):
        self.ax1.clear()
        self.ax1.plot(inputValInt,inputValInt1)
        try:
            last = len(inputValInt)
            lastVal = inputValInt[last-1]
            self.ax1.set_xlim([0+lastVal-aquisitionTime  ,lastVal]   ) #comment for no x axis mouvement
        except:
            print("")
        self.get_data()  

    def get_data(self):
        global inputValUtf
        global inputMaxVal
        global inputMaxValStr
        while self.arduino.inWaiting():
            buff = self.arduino.readline()
            self.serialInput.text = buff
            #print(buff.decode('utf-8'))
            #print(buff.split())
            inputVal = buff.split()
            #print(buff)
            #print(inputValUtf[0])
            #print(inputValUtf[1])
            #print(inputValInt)
            
            
            try:
                inputValUtf = [inputVal[0].decode('utf-8'),inputVal[1].decode('utf-8')]
                if inputMaxVal< int(inputValUtf[1]):
                    inputMaxVal= int(inputValUtf[1])
                    inputMaxValStr = inputValUtf[1]
                    self.maxLabel.text = 'max: '+inputMaxValStr
            except:
                print("")   
            try:
                inputValInt.append(int(inputValUtf[0]))
                inputValInt1.append(int(inputValUtf[1]))
            except:
                print("")


            self.fichier.write(buff)
            self.fig.canvas.draw()
            #plt.show()

    def serialWrite(self,)
    
    def serial_ports(self):
        """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
         """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
        
   
MyApp().run()