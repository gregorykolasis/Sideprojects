import os
import sys
import subprocess
import time
try:
    import wmi
except ModuleNotFoundError:
    os.system("pip install wmi")
    os.execv(sys.executable, ['python'] + sys.argv) 

'''
    Windows users only
    1. Settings -> Change User Account Control Settings -> Never notify me when ...
'''

# PYTHON_PATH         = "python"                     #r"C:\Users\intelligent69\AppData\Local\Programs\Python\Python39\python.exe"
# CHECKER_SCRIPT_PATH = f"{path}/startupPrograms.py" #C:\Users\intelligent69\Desktop\OpenStartUpPrograms\checkStartupPrograms.py"
programsNotOpened = []
path = os.path.abspath(os.path.join(__file__, "../"))

#--------------------------------------------CONFIGURATION----------------------------------------------
SECONDS_SLEEP  = 30
IDLE_TIME      = 5                                   #Seconds to wait for Processor CPU Usage < IDLE_PERCENT , meaning the PC completed startup
IDLE_PERCENT   = 30                                  #Proccessor CPU Usage 
startUpPrograms = ['laragon.exe','AnyDesk.exe']
#--------------------------------------------CONFIGURATION----------------------------------------------

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

#============================================================================================================================

def get_load():
    output = subprocess.check_output('wmic cpu get loadpercentage', shell=True)
    load = output.split()[1]
    return int(load)

def openPrograms():
    #subprocess.call([PYTHON_PATH,CHECKER_SCRIPT_PATH])
    print("Checking...")
    for x in startUpPrograms:
        checkProcessRunning(x)
    for z in programsNotOpened:
        startPrograms(z)

def waitTillReady():
    idleSeconds = 0
    while idleSeconds < IDLE_TIME:
        load = get_load()
        print(f"CPU Usage:{load}% | {IDLE_TIME-idleSeconds} seconds until openPrograms")
        if load < IDLE_PERCENT:
            idleSeconds += 1
        else:
            idleSeconds = 0
        time.sleep(1)

if __name__ == "__main__":
    print(f"[monitorStartup] Waiting for {SECONDS_SLEEP} seconds before running...")
    time.sleep(SECONDS_SLEEP)
    waitTillReady()
    try:
        openPrograms()
    except Exception as e:
        print(f"openPrograms() Failed with Error:{e}")