import serial

class SerialConnection(object):
	def __init__(self,comPort, baudRate = 9600, timeOut = 1)
		self.port = comPort
		self.bRate = baudRate
		self.tOut = timeOut

	def beginSerial(self):
		connectionStatus = False
		try:
			self.serialDevice = serial.Serial(self.port, self.baudRate, self.timeOut)
			connectionStatus = True
			logger.info("Connected")
		except:
			connectionStatus = False
			logger.info("Can't connect. Select an other com port")
		return connectionStatus

	def stopSerial(self):
		try:
            self.arduino.close()
            logger.info("Disconnected properly")
        

	def resetSerial(self):

    def serial_ports(self):
