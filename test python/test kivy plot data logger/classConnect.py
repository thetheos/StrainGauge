
import serial
import logging

class SerialConnection(object):
    

    def __init__(self,comPort, baudRate = 9600, timeOut = 1):
        self.port = comPort
        self.bRate = baudRate
        self.tOut = timeOut
        self.connectionStatus = False
        self.serialLogger()
        print(self)

    def beginSerial(self):
        try:
            self.serialDevice = serial.Serial(self.port, self.baudRate, self.timeOut)
            self.connectionStatus = True
            self.logger.info("Connected")
        except:
            self.connectionStatus = False
            self.logger.info("Can't connect. Select an other com port")
        

    def stopSerial(self):
        """
            Stop serial connection and Stop the data logging
        """
        try:
            self.serial.close()
            self.logger.info("Disconnected properly")
        except:
            self.logger.info("Can't disconnect. Try to connect before disconnect")
        

    def resetSerial(self):
        """
            Reset serial connection
        """
        try:
            self.stopSerial()
            self.beginSerial()
        except:
            self.logger.info("can't reset. Try to connect before reset")
    
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

    def serialStatus(self):
        return self.connectionStatus

    def serialLogger(self):
        loggingFormat =logging.Formatter('%(asctime)s -- %(levelname)s -- %(funcName)s -- %(lineno)d -- %(message)s')
        handler_info = logging.StreamHandler()
        handler_info.setFormatter(loggingFormat)
        handler_info.setLevel(logging.INFO)
        self.logger = logging.getLogger("__name__")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler_info)

if __name__=='__main__':
    arduino = SerialConnection('COM5')
    a2 = SerialConnection('COM4')
    print(a2.serial_ports())
    print(a2.serialStatus())
    arduino.beginSerial()
    arduino.stopSerial()
    arduino.resetSerial()
    print(arduino.serialStatus())
