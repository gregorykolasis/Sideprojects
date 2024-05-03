import subprocess
import time

IDLE_TIME    = 5  #Seconds to wait for Processor CPU Usage < IDLE_PERCENT , meaning the PC completed startup
IDLE_PERCENT = 30 #Proccessor CPU Usage 

PYTHON_PATH         = r"C:\Users\intelligent69\AppData\Local\Programs\Python\Python39\python.exe"
CHECKER_SCRIPT_PATH = r"C:\Users\intelligent69\Desktop\OpenStartUpPrograms\checkStartupPrograms.py"

def get_load():
    output = subprocess.check_output('wmic cpu get loadpercentage', shell=True)
    load = output.split()[1]
    return int(load)

def openPrograms():
    subprocess.call([PYTHON_PATH,CHECKER_SCRIPT_PATH])

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
    waitTillReady()
    try:
        openPrograms()
    except Exception as e:
        print(f"openPrograms() Failed with Error:{e}")