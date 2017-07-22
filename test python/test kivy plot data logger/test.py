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
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from functools import partial
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
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

import logging

buff = 0
inputVal = ['100','100'] #obliger d'initialiser le tableau
inputValInt = [0,10]
inputValInt1= [0,10]
inputValUtf = [0,0]
aquisitionTime= 1000 #default 1000, Set the delta scale for the x axis
inputMaxVal = 0
inputMaxValStr = "max: NaN"
lastComPort = ""
dataFileCheckBoxState = 0


loggingFormat =logging.Formatter('%(asctime)s -- %(levelname)s -- %(funcName)s -- %(lineno)d -- %(message)s')

handler_info = logging.StreamHandler()

handler_info.setFormatter(loggingFormat)

handler_info.setLevel(logging.INFO)

logger = logging.getLogger("__name__")
logger.setLevel(logging.INFO)
logger.addHandler(handler_info)


            



#TODO add a checkbox for the data logging and maybe add a fille explorer
#to define the storage
#TODO setup a second layout with the command to the arduino
#TODO add a connection verigication with the arduino to be sure it is the
#arduino and not an other device
#TODO modify the layouts to make it mych "nicer"
#TODO add an auto connect with the log of the last comport used
#in a config text file. Easyer to use.
#TODO Add a gunction to clear the data when the arduino is deconected or
#manually resetted
#TODO add an other logger for critic and error level to log into a file
#TODO make it portable on android
#TODO try to solve the glitch problem on startup
#TODO write a md file for installation
#TODO try to solve runTime event error when close
#TODO add the oportunity to set a specific file name for the data file
#TODO add a setting menu as well for kivy than for the arduino to setup 
#eeprom value.
#TODO on arduino change the settings variable to eeprom variable

        

class MyApp(App):
    def callbackSearchSerialPort(self,instance):
            self.searchSerialPorts()

    def beginSerialCallback(self, instance):
        global lastComPort
        self.stopSerial()
        try:
            self.beginSerial(instance.text)
            lastComPort = instance.text
            logger.info("last com port: %s", lastComPort)
            self.connectionStatus.text="Connected"
            logger.info("Serial connected to %s", instance.text)
            self.buttonBeginSerial.disabled = True
            self.checkBoxDataLogging.disabled = True
            self.serialPopup.dismiss()
            
        except:
            self.connectionStatus.text="Connection error"
            logger.error("Serial connection error")

    def callbackStopSerial(self, instance):
        self.stopSerial()

    def callbackResetSerial(self, instance):
        self.resetSerialConnection()

    def on_checkbox_active(self, checkbox, value):
        global dataFileCheckBoxState
        dataFileCheckBoxState = value

    def callback1(self, instance):
        self.clearData()

    def continuousCallback(self, instance):
        self.arduino.write('1\n')

    def triggerCallback(self, instance):
        self.arduino.write('2\n')

    def settingsCallback(self, instance):
        self.arduino.write('3\n')

    def build(self):
        self.buildPlot()
        
        self.box = FloatLayout(size = (300,300))
        self.box1 = BoxLayout()
        self.serialPopup = Popup(title = 'Chose Serial port', content = Label(text = 'Choose serial port'),size_hint=(None, None), size =(400,400))

        self.plotter = FigureCanvasKivyAgg(plt.gcf(), size_hint = (0.75,0.6), pos_hint ={'center_x':.5, 'top':.97})
        self.buttonBeginSerial = Button(text="Begin Serial", font_size=14,size_hint = (.1,.1), pos_hint = {'left':1, 'bottom':1})
        self.buttonBeginSerial.bind(on_press= self.callbackSearchSerialPort)
        self.buttonStopSerial = Button(text= "Stop Serial", font_size= 14, size_hint=(.1,.1), pos_hint= {'center_x':.5, 'bottom':1})
        self.buttonStopSerial.bind(on_press= self.callbackStopSerial)
        self.buttonResetSerial = Button(text= "Reset Serial", font_size= 14, size_hint=(.1,.1), pos_hint= {'center_x':.75, 'bottom':1})
        self.buttonResetSerial.bind(on_press= self.callbackResetSerial)

        self.buttonWippeDate = Button(text = "wippe data", font_size=14, size_hint=(0.1,0.1), pos_hint = {'right':1, 'bottom':1})
        self.buttonWippeDate.bind(on_press=self.callback1)
        self.maxLabel= Label(text="max: NaN",font_size=48,pos_hint = {'center_x':.5, 'top':.8})
        self.serialInput = Label(text="Serial input:", font_size=48, pos_hint ={'center_x':.7,'top':.8})
        self.buttonContinuousMode = Button(text = "Continuous mode", font_size = 14, size_hint=(.1,.1))
        self.buttonContinuousMode.bind(on_press=self.continuousCallback)
        
        self.checkBoxDataLogging = CheckBox(size_hint = (.1,.1),pos_hint={'center_x':.25, 'bottom':1})
        self.checkBoxDataLogging.bind(active = self.on_checkbox_active)

        self.buttonTriggerMode = Button(text = "Trigger mode", font_size = 14, size_hint=(.1,.1))
        self.buttonTriggerMode.bind(on_press=self.triggerCallback)
        
        self.buttonSettingsMode = Button(text = "Settings mode", font_size = 14, size_hint=(.1,.1))
        self.buttonSettingsMode.bind(on_press=self.settingsCallback)
    
        self.box.add_widget(self.plotter)
        self.box.add_widget(self.buttonBeginSerial)
        self.box.add_widget(self.buttonStopSerial)
        self.box.add_widget(self.buttonResetSerial)
        self.box.add_widget(self.buttonWippeDate)
        self.box.add_widget(self.maxLabel)
        self.box.add_widget(self.serialInput)
        self.box.add_widget(self.checkBoxDataLogging)

        self.box1.add_widget(self.buttonContinuousMode)
        self.box1.add_widget(self.buttonTriggerMode)
        self.box1.add_widget(self.buttonSettingsMode)

        logger.info("running")
        return self.box

    def createDataFile(self, fileName=time.strftime("%Y-%m-%d_%H-%M-%S")):
        """generate a file to log the data with as filename the date and time
        """
        self.fichier = open('data'+fileName+ '.txt', 'wb')

    def searchSerialPorts(self):
        """
            search serial ports and open a popup window in kivy the select the ports.
            The buttons are automatically created in functions of the number of ports
        """
        logger.info('%s',self.serial_ports())
        i=0
        serialButton =[]
        self.serialBox = BoxLayout(orientation = 'vertical')
        self.connectionStatus = Label(text="choose port")
        self.serialBox.add_widget(self.connectionStatus)
        for ports in self.serial_ports(): 
            serialButton.append(Button(text= ports, auto_dismiss = True ))
            serialButton[i].bind(on_press=self.beginSerialCallback)
            self.serialBox.add_widget(serialButton[i])
            i+=1
            #print(ports)
        self.serialPopup.content = self.serialBox
        self.serialPopup.open()
    
    def beginSerial(self, serialPort):
        """
            Begin serial connection and create data logging file
        """
        global dataFileCheckBoxState
        self.arduino = serial.Serial(serialPort, 9600, timeout=1)
        if dataFileCheckBoxState:
            self.createDataFile(fileName=time.strftime("%Y-%m-%d_%H-%M-%S"))
        self.updateAnimate = Clock.schedule_interval(self.animate,0)

    
    def stopSerial(self):
        """
            Stop serial connection and Stop the data logging
        """
        global dataFileCheckBoxState
        self.clearData()
        try:
            self.arduino.close()
            if dataFileCheckBoxState:
                self.fichier.close()
            Clock.unschedule(self.updateAnimate)
            logger.info("Serial connection stopped")
            self.buttonBeginSerial.disabled = False
            self.checkBoxDataLogging.disabled = False
        except:
            logger.warning("Begin Serial before stopping it")

    def resetSerialConnection(self):
        global lastComPort
        try:
            self.stopSerial()
            logger.info('lCp %s', lastComPort)
            self.beginSerial(lastComPort)
            logger.info("Serial connection resetted")
        except:
            logger.warning("Begin Serial before resetting it")



    def buildPlot(self):
        """
            Set desing for the plot and use the aquisitions lists to plot.
        """
        style.use('fivethirtyeight')
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.ax1.clear()
        self.ax1.plot(inputValInt,inputValInt1)

    def clearData(self):
        """
            Wippe the aquisitions lists for the plotting
        """
        global inputMaxVal
        del inputValInt[:]
        del inputValInt1[:]
        inputMaxVal = 0
        self.maxLabel.text = "max: NaN"
        logger.info("data wipped")


    def animate(self,dt):
        """
            Update the plotting with the 2 lists inputValInt and inputValInt1.
            Change the scale of x axis by modifying constantly the set_xlim.

        """
        self.ax1.clear()
        self.ax1.plot(inputValInt,inputValInt1)
        try:
            last = len(inputValInt)
            lastVal = inputValInt[last-1]
            self.ax1.set_xlim([0+lastVal-aquisitionTime  ,lastVal]) #comment for no x axis mouvement. Aquisition time is for the scale delta
        except:
            last = 0
            logger.warning("unable to get correct input val")
        self.get_data()  

    def get_data(self):
        """
            While serial connection is available, it prints readline(to file and monitor), decode it and create 2 list: each contains respectivelly x and y.
            In this case inputValInt is the x axis for time(ms) and inputValInt1 is the y axis for the analogRead
            The lists contains all the data that has been read.. And it is used for the plotting.
            The serial input must be 2 values separated by a tab (\n) and must end with the endline character (\n).

         """
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
                logger.warning("unable to convert to utf-8")   
            try:
                inputValInt.append(int(inputValUtf[0]))
                inputValInt1.append(int(inputValUtf[1]))
            except:
                logger.warning("unable to convert to int")


            self.fichier.write(buff)
            self.fig.canvas.draw()
            #plt.show()

    
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