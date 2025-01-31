import functools
import os
import sys
import asyncio
import threading
import subprocess
import logging
import datetime

from libs.utils import getPlatform
from libs.mySerial import mySerial
from libs.myKeyboard import myKeyboard
from libs.myLogger import setLogger
from libs.myRS485Programmer import myRS485Programmer

path = os.path.abspath(os.path.join(__file__, "../"))

class Programmer( mySerial , myKeyboard , myRS485Programmer ):

    buildfile = 'Unknown'
    port  = 'Unknown'
    skip        = 'No'
    interactive = 'Yes'
    portInsertedByUser = False

    DEV   = False
    
    def __init__(self, loop=None):
        self.loop = loop  
        #self.mainLoop()

    def setupLogger(self,loggingType,customFormatter):
        filename = f"{path}/logs/{__name__}.log"  
        setLogger(filename,loggingType,customFormatter)
        self.logger = logging.getLogger()

    def readArgvs(self):
        gotArgs = False
        try:
            args = sys.argv
            try:
                _tempStr = str(args[1])
                _tempStr = _tempStr.replace("port","")
                _tempStr = _tempStr.replace("=","")
                self.port = _tempStr
                self.portInsertedByUser = True
                gotArgs = True
            except Exception as e:
                pass
            try:
                _tempStr = str(args[2])
                _tempStr = _tempStr.replace("skip","")
                _tempStr = _tempStr.replace("=","")
                self.skip = _tempStr
                gotArgs = True
            except Exception as e:
                pass
            try:
                _tempStr = str(args[3])
                _tempStr = _tempStr.replace("interactive","")
                _tempStr = _tempStr.replace("=","")
                self.interactive = _tempStr
                gotArgs = True
            except Exception as e:
                pass
        except Exception as e:
            print(e)
        return gotArgs

    def chooseBuildFile(self,isInteractive):
        ext = ('ino.bin')
        allBuilds = []
        chosenBuildFile = None
        buildPath = f"{path}/Build"
        for files in os.listdir(buildPath):
            if files.endswith(ext):
                filename = files.split(".", 1)[0]
                allBuilds.append(filename)
            else:
                try:
                    print(f"Removing that useless file:{files}")
                    removedFilepath = f"{buildPath}/{files}"
                    if os.path.isfile(removedFilepath):
                        os.remove(removedFilepath)
                except Exception as e:
                    print(f"Couldn't remove useless file:{files} with Error:{e}")
        lenBuilds = len(allBuilds)
        if lenBuilds>1:
            if isInteractive:
                print("More than 1 buildfile detected!")
                for i,v in enumerate(allBuilds):
                    print(f"{i+1}. {v}")     
                chosenBuild = input(f"Please choose the buildfile , Type a number from 1 to {lenBuilds} and then press Enter !\n")
                num = int(chosenBuild)
                if num!=0 and num<=lenBuilds and num!=0:
                    chosenBuildFile = allBuilds[num-1]
                    print(f"You choose the buildfile: {chosenBuildFile}")
                else:
                    print(f"Wrong number:{num}")
            else:
                modifiedFiles = []
                print(f"Will find the most recent buildfile and choose this")
                for x in allBuilds:
                    m_time = os.path.getmtime(f'{buildPath}/{x}.ino.bin')
                    dt = datetime.datetime.fromtimestamp(m_time)
                    #print(f"buildfile:{x} | modified at:{dt}")
                    modifiedFiles.append({"Filename":x,"Modified":dt})
                chosenBuildFile = max(modifiedFiles, key = lambda x: x["Modified"])["Filename"]
        else:
            chosenBuildFile = allBuilds[0]
        return chosenBuildFile
        
    def findBuildName(self): #not used
        checkName='Unknown'
        ext = ('.bin','.elf','.map')
        for files in os.listdir(f"{path}/Build"):
            if files.endswith(ext):
                cutName = files.split(".", 1)
                if checkName=='Unknown':
                    checkName=cutName[0]
                elif not (cutName[0]==checkName):
                    sys.exit(f"Your build folder consist of different file-names. Please fix it!\n 1:{cutName[0]} 2:{checkName}")
        return checkName

    async def startProgrammer(self,isInteractive):
        if self.portInsertedByUser == False: 
            self.logger.critical("==========Gonna seach Port myself")
            await self.findCOM()
        else:
            if not self.port in str(self.getAllPorts()):
                sys.exit(f"Can't find PORT:{self.port}")
        try:
            await self.open_connection(searchPort=False)
            firmwareFileFullPath = f"{path}/Build/{self.buildfile}.ino.bin"
            self.loop.create_task(self.update_firmware(filePath = firmwareFileFullPath, slave_address = 1 , bus_num = 0))
        except Exception as e:
            print(f"[ERROR]: Exiting with returnCode:{1} Errors:{e}")
            self.loopCleanup()
            sys.exit(1)
        
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
        gotArgs = self.readArgvs()
        if self.interactive == 'Yes': isInteractive = True
        else: isInteractive = False
        self.setupLogger(logging.INFO,customFormatter=isInteractive)
        if gotArgs:
            print(f"[Argument] port:{self.port}")
            print(f"[Argument] skip:{self.skip}")
            print(f"[Argument] interactive:{self.interactive}")
        try:
            myRS485Programmer.__init__(self, self.loop)        
            mySerial.__init__(self, loop = self.loop, searchPort = False , openConnection = False )      
            self.sendSerial = self.serialSend
            myKeyboard.__init__(self, self.loop)                  
        except Exception as e:
            self.logger.error(e)
        self.platform = getPlatform()
        self.buildfile = self.chooseBuildFile(isInteractive) #self.findBuildName()
        asyncio.run_coroutine_threadsafe(self.startProgrammer(isInteractive),self.loop)
        self.loop.run_forever() #With this way it will only say command executed Sucessfully       

              
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    myProgrammer = Programmer(loop)
    myProgrammer.mainLoop()
    
