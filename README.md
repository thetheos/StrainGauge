View this project on [CADLAB.io](https://cadlab.io/project/1158). 

# StrainGauge

Here is a proto shield for arduino uno to easily mount strain gauges. It uses the pin A1 to read the output of the instrumental
amp (ina125p).

I wrote also a small program wich can read the input of the signal on pin A1 and rewrite it on the serial monnitor (9600 baud). 
There is 2 mode of reading:
-Continuous reading (read in continuous...)
-Triger mode read: print data only when the strain gage is stressed. The triger mode settings can be modified in the program via serial
monitor (both the sensitivity of the triger and the sample rate).

This project was designed to measure the thrust power of a propellant motor.
