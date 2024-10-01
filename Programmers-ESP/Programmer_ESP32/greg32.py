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

path = os.path.abspath(os.path.join(__file__, "../"))

def printStd(stream, label):
    while True:
        line = stream.readline()
        if line:
            print(f"{label}: {line.strip()}")
        else:
            break

def executeSubprocess(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, shell=True)
    printStdout = threading.Thread(target = printStd , args = (process.stdout, "[INFO]") )
    printStderr = threading.Thread(target = printStd , args = (process.stderr, "[ERROR]") )
    printStdout.start(); 
    printStderr.start(); 
    printStdout.join()
    printStderr.join()
    process.wait()
    return process.returncode

class Programmer( mySerial , myKeyboard ):

    port  = 'Unknown'
    baud  = '2000000'
    flash = 4 #MB
    buildfile = 'Unknown'

    skip        = 'No'
    interactive = 'Yes'

    DEV   = False
    portInsertedByUser = False
    
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
        

    def findBuildName(self):
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

    def createProgrammingCmd(self):
        command = ''
        esptoolType = "Unknown"
        if self.platform == "windows" : esptoolType = "exe"
        if self.platform == "linux"   : esptoolType = "py"
        esptool = f"{path}/tools/apps/esptool.{esptoolType} --chip esp32 --port {self.port} --baud {self.baud} --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size {self.flash}MB"
        bootBin       = f"0xe000 {path}/tools/memoryfiles/boot_app0.bin"
        bootloaderBin = f"0x1000 {path}/tools/memoryfiles/{self.flash}MB/{self.flash}MB.ino.bootloader.bin"
        partitionsBin = f"0x8000 {path}/tools/memoryfiles/{self.flash}MB/{self.flash}MB.ino.partitions.bin"
        mainBin       = f"0x10000 {path}/Build/{self.buildfile}.ino.bin"
        if self.platform == "windows" : command = f"{esptool} {bootBin} {bootloaderBin} {mainBin} {partitionsBin}"
        if self.platform == "linux"   : command = f"sudo python3 {esptool} {bootBin} {bootloaderBin} {mainBin} {partitionsBin}" 
        return command
    
    async def startProgrammer(self,isInteractive):
        if self.portInsertedByUser == False: 
            self.logger.critical("==========Gonna seach Port myself")
            await self.findCOM()
        else:
            if not self.port in str(self.getAllPorts()):
                sys.exit(f"Can't find PORT:{self.port}")
        try:
            self.logger.warning(f"===========Programming the buildfile: {self.buildfile}==========")
            if isInteractive:
                returnCode = os.system( self.createProgrammingCmd() )   
            else:
                returnCode = executeSubprocess( self.createProgrammingCmd() )   
            if self.skip != 'No': 
                print(self.skip)
                print(f"[INFO]: Exiting with returnCode:{returnCode}")
                self.loopCleanup()
                sys.exit(returnCode)
        except Exception as e:
            print(f"[ERROR]: Exiting with returnCode:{1} Errors:{e}")
            self.loopCleanup()
            sys.exit(1)
        await self.open_connection(searchPort=False)

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
            mySerial.__init__(self, loop = self.loop, searchPort = False , openConnection = False )      
            self.sendSerial = self.serialSend
            myKeyboard.__init__(self, self.loop)        
        except Exception as e:
            self.logger.error(e)
        self.platform = getPlatform()
        self.buildfile = self.chooseBuildFile(isInteractive) #self.findBuildName()
        asyncio.run_coroutine_threadsafe(self.startProgrammer(isInteractive),self.loop)
        # if isInteractive:
        #     try:
        #         self.loop.run_forever()         
        #     except Exception as e:
        #         print(f'[{__name__}] Error {e}')
        #     finally:
        #         print(f'[{__name__}] Error Finally')
        #         sys.exit("Exiting...")
        # else:
        self.loop.run_forever() #With this way it will only say command executed Sucessfully       

              
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    myProgrammer = Programmer(loop)
    myProgrammer.mainLoop()
    
