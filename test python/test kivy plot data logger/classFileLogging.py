import logging
import time


class FileLogging(object):
    
    def __init__(self, fileName = 'data'+time.strftime("%Y-%m-%d_%H-%M-%S"), logLevel = 'INFO'):
        self.log = logLevel#respect the order because method open()
        self.fileLogger()#requires filelogger
        self.fName = fileName
        self.open()
        
    def open(self):
        """
            generate a text file with default name the time
        """
        try:
            self.fichier = open(self.fName+'.txt','w')
            self.logger.info("file created/open")
        except:
            self.logger.error("unable to create/open file")

    def close(self):
        """
            close file
        """
        try:
            self.fichier.close()
            self.logger.info("File closed")
        except:
            self.logger.error("can't close file. Create a file before closing it")

    def write(self,data=None):
        """
            write data to the file
        """
        try:
            self.fichier.write(data)
            self.logger.info("data wrotten to the file")
        except:
            self.logger.error("unable to write data to the file")

    def fileLogger(self):
        """
            create log object for this class
        """
        loggingFormat =logging.Formatter('%(asctime)s -- %(levelname)s -- %(funcName)s -- %(lineno)d -- %(message)s')
        handler_info = logging.StreamHandler()
        handler_info.setFormatter(loggingFormat)
        handler_info.setLevel(logging.INFO)
        self.logger = logging.getLogger("__name__")
        self.logger.setLevel(self.log)
        self.logger.addHandler(handler_info)

if __name__ == '__main__':
    f1 = fileLogging('INFO')
    f1.open()
    f1.write('ceci est un test')
    f1.close()