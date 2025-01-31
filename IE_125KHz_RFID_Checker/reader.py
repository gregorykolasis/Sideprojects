import functools
import os
import sys
import asyncio
import threading
import subprocess
import logging
import datetime
import json
import time
from threading import Timer

from libs.utils import getPlatform
from libs.mySerial import mySerial
from libs.myKeyboard import myKeyboard
from libs.myLogger import setLogger

path = os.path.abspath(os.path.join(__file__, "../"))

class Logger(mySerial, myKeyboard):

    initTimer = None

    def __init__(self, loop=None):
        self.loop = loop  
        self.rfid_data_file = f"{path}/rfid.json"
        self.duplicates_data_file = f"{path}/duplicates.json"
        self.load_rfid_data()
        self.load_duplicates_data()
        #self.mainLoop()

    LOGFILE_NAME = 'RFID'
    SESSION_LOGGING = True
    port = 'COM4'

    def load_rfid_data(self):
        # Load existing RFID data from JSON file, or create an empty dictionary if the file doesn't exist
        if os.path.exists(self.rfid_data_file):
            with open(self.rfid_data_file, 'r') as f:
                try:
                    self.rfid_data = json.load(f)
                except json.JSONDecodeError:
                    self.rfid_data = {}
        else:
            self.rfid_data = {}

    def load_duplicates_data(self):
        # Load existing duplicates data from JSON file, or create an empty dictionary if the file doesn't exist
        if os.path.exists(self.duplicates_data_file):
            with open(self.duplicates_data_file, 'r') as f:
                try:
                    self.duplicates_data = json.load(f)
                except json.JSONDecodeError:
                    self.duplicates_data = {}
        else:
            self.duplicates_data = {}

    def save_rfid_data(self):
        # Save the current RFID data to JSON file
        with open(self.rfid_data_file, 'w') as f:
            json.dump(self.rfid_data, f, indent=4)

    def save_duplicates_data(self):
        # Save the current duplicates data to JSON file
        with open(self.duplicates_data_file, 'w') as f:
            json.dump(self.duplicates_data, f, indent=4)

    def getSerial(self, msg):
        print(f"[Serial-Recieve]{msg}")
        type = 'Nojson'
        numToColor = {
            1: "Red",
            2: "Purple",
            3: "Green",
            4: "Yellow",
            5: "Blue",
            6: "Orange"
        }

        if len(msg)<2: return;

        try:
            data = json.loads(msg)
            type = data["type"]
        except Exception as e:
            data = msg
        if type=='rfid':
            try:
                rfidFull     = str(data['id'])
                id           = int(rfidFull[1:]) 
                colorInteger = int(rfidFull[0])
                colorString = "Unknown"
                if colorInteger > 0 and colorInteger <= 6: 
                    colorString = numToColor[colorInteger]  
                if str(id) in self.rfid_data:
                    existing_color = self.rfid_data[str(id)]["color"]
                    if existing_color == colorString:
                        # Same RFID wristband with the same color
                        self.logger.warning(f"[RFID-Bracelet] WARNING: Wristband with ID:{id} and Colour:{colorString} is already registered.")
                    else:
                        # Same RFID wristband with a different color
                        self.logger.error(f"[RFID-Bracelet] ERROR: Wristband with ID:{id} is already registered with a different Colour. Existing Colour: {existing_color}, New Colour: {colorString}")
                        # Save the duplicate information
                        now = datetime.datetime.now()
                        timeNow = now.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]
                        self.duplicates_data[str(id)] = {
                            "existing_color": existing_color,
                            "new_color": colorString,
                            "timestamp": timeNow
                        }
                        self.save_duplicates_data()
                else:
                    # Register new RFID wristband
                    now = datetime.datetime.now()
                    timeNow = now.strftime('%d/%m/%Y %H:%M:%S.%f')[:-3]
                    self.rfid_data[str(id)] = {
                        "color": colorString,
                        "timestamp": timeNow
                    }
                    self.save_rfid_data()
                    self.logger.critical(f"[RFID-Bracelet] SUCCESS Wristband with ID:{id} and Colour:{colorString} is saved.")
            except Exception as e:
                self.logger.error(f"[RFID-Bracelet] ERROR: {msg}")
        
    def sendSerial(self, msg):
        self.serialSend(f"{msg}#")
        
    def initCommunication(self):
        msg = {"type":"Simple-Actions","payload":"Get-Information"}
        self.sendSerial(json.dumps(msg))
        time.sleep(1)
        msg = {"type":"Scan-Init","rx":5}
        self.sendSerial(json.dumps(msg))

    def setupLogger(self, loggingType, customFormatter):
        # myLogger.__init__(self)  
        if self.SESSION_LOGGING:
            now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            date = datetime.datetime.now().strftime('%Y_%m_%d')
            subFolder = f"{self.LOGFILE_NAME}_Session_{date}"
            subFolderPath = f"{path}/logs/{subFolder}"
            isExist = os.path.exists(subFolderPath)
            if not isExist:
                os.makedirs(subFolderPath)
            filename = f"{subFolderPath}/{self.LOGFILE_NAME}_{now}.log" 
        else:
            filename = f"{path}/logs/{self.LOGFILE_NAME}.log"  
        if self.SESSION_LOGGING: print('[Main]This script is using SESSION_LOGGING')   
        setLogger(filename, loggingType, customFormatter)
        self.logger = logging.getLogger()

    def loopCleanup(self):
        try:
            print('Cleaning up...')
            # Cancel all tasks running on the loop
            tasks = asyncio.all_tasks(self.loop)
            for task in tasks:
                task.cancel()
            # Ensure all tasks are cancelled and gather them to complete their cancellation processes
            self.loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
            # Only attempt to stop the loop if it is running
            if self.loop.is_running():
                self.loop.stop()
            # Finally, close the loop
            self.loop.close()
        except Exception as e:
            pass

    def mainLoop(self):     
        isInteractive = True
        self.setupLogger(logging.INFO, customFormatter=isInteractive)
        try:
            mySerial.__init__(self, loop=self.loop, searchPort=False, openConnection=True, baudrate=115200)      
            self.sendSerial = self.serialSend
            #myKeyboard.__init__(self, self.loop) 
            self.initTimer  = Timer(0.5,self.initCommunication); self.initTimer.start()
        except Exception as e:
            self.logger.error(e)
        self.platform = getPlatform()
        self.loop.run_forever()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    myProgrammer = Logger(loop)
    myProgrammer.mainLoop()
