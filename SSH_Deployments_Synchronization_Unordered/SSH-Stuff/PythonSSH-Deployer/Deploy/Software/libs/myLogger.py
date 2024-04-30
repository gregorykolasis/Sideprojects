
import sys 
import logging 
from logging.handlers import RotatingFileHandler


class myLogger:
    def __init__(self):
        print('[Logger]Init')
    def setLogger(self , filename, name="TheCrazyLogger" , level=logging.INFO):
        tempLogger = logging.getLogger(name)       
        tempLogger.setLevel(level)   
        print(f"[Logger]Full path:{filename}")  
        output_file_handler = RotatingFileHandler(f"{filename}", maxBytes=2000000, backupCount=10)
        console_handler = logging.StreamHandler(sys.stdout)
        debug_format = logging.Formatter('[%(levelname)s] | [%(asctime)s] | %(message)s',"%Y-%m-%d %H:%M:%S") 
        #logging.Formatter('[%(asctime)s] | Level:%(levelname)s | %(message)s',"%Y-%m-%d %H:%M:%S")
        output_file_handler.setFormatter(debug_format)
        console_handler.setFormatter(debug_format)
        if not logging.getLogger(name).hasHandlers():
            tempLogger.addHandler(output_file_handler)
            tempLogger.addHandler(console_handler)   
        tempLogger.propagate = False
        return tempLogger      
    def initLogger(self,filename):
        self.logger = self.setLogger(filename=filename)