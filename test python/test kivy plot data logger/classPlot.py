import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
#matplotlib.use('Gtk')
import numpy                                as np
import matplotlib.pyplot                    as plt
import matplotlib.animation                 as animation
from matplotlib                             import style
from kivy.app                               import App
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock                             import Clock
from kivy.uix.dropdown                      import DropDown
from kivy.base                              import runTouchApp
from kivy.uix.floatlayout                   import FloatLayout

import logging

class SerialPlotter(App):

    def __init__(self,inVal = [1,2], inval1 = [1,2]):
        self.inputValInt = inVal
        self.inputValInt1 = inval1
        App.__init__(self)
        
    def build(self):
        print('run')
        self.buildPlot()
        self.plotter = FigureCanvasKivyAgg(plt.gcf(), size_hint = (0.75,0.6), pos_hint ={'center_x':.5, 'top':.97})
        return self.plotter

    def update(self):
        self.updateAnimate = Clock.schedule_interval(self.animate,0)

    def stopUpdate(self):
        Clock.unschedule(self.updateAnimate)
        
    def animate(self,dt):
        """
            Update the plotting with the 2 lists inputValInt and inputValInt1.
            Change the scale of x axis by modifying constantly the set_xlim.

        """
        self.ax1.clear()
        self.ax1.plot(self.inputValInt,self.inputValInt1)
        try:
            last = len(self.inputValInt)
            lastVal = self.inputValInt[last-1]
            self.ax1.set_xlim([0+lastVal-aquisitionTime  ,lastVal]) #comment for no x axis mouvement. Aquisition time is for the scale delta
        except:
            last = 0
            logger.warning("unable to get correct input val")
        self.get_data() 

    def buildPlot(self):
        """
            Set desing for the plot and use the aquisitions lists to plot.
        """
        style.use('fivethirtyeight')
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.ax1.clear()
        self.ax1.plot(self.inputValInt,self.inputValInt1)

if __name__ == '__main__':
    g1 = SerialPlotter([2,3],[5,6])
    b1 = FloatLayout()
    FloatLayout().run()


 