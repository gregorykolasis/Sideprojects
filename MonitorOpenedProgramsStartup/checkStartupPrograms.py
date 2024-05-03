import os
import sys
import subprocess
import time
try:
    import wmi
except ModuleNotFoundError:
    os.system("pip install wmi")
    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 

IDLE_TIME = 5
IDLE_PERCENT = 30

startUpPrograms = ['laragon.exe','AnyDesk.exe']
programsNotOpened = []

def checkProcessRunning(ProgramName):
    if(wmi.WMI().Win32_Process(name=ProgramName)):
        print(ProgramName + " is running")
    else:
        print(ProgramName + " is not running")
        programsNotOpened.append(ProgramName)

def findFileLocation(ProgramName):
    for root, dirs, files in os.walk('C:\\'):
        if ProgramName in files:
            return root
    return None

def startPrograms(ProgramName):
    file_location = findFileLocation(ProgramName)
    
    if file_location:
        print(f"Found {ProgramName} at the following location:")
        print(file_location)
        program_path = os.path.join(file_location, ProgramName)
        os.startfile(program_path)
    else:
        print(f"Could not find {ProgramName}")
  
if __name__ == "__main__":
    print("Checking...")
    for x in startUpPrograms:
        checkProcessRunning(x)
    for z in programsNotOpened:
        startPrograms(z)