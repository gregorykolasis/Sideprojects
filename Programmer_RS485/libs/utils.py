import socket
from time import time
from time import sleep
from random import *
import re,uuid
import os,sys

def getPlatform():
    if sys.platform=="linux" or sys.platform=="linux2":
        return "linux"
    elif sys.platform == "win32":
        return "windows"

def restartScript():
    print("argv was",sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")
    os.execv(sys.executable, ['python'] + sys.argv)

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False
    
def myIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP        
    
def myTimestamp():
    return (int(round(time()*1000)))

def myMAC():
	try:
		import getmac
		return getmac.get_mac_address()
	except ModuleNotFoundError:
		os.system("pip install getmac")
		import getmac
		return getmac.get_mac_address()

def powerOff(type):
    if type=='SHUTDOWN':
        try:
            os.system('sudo poweroff')
        except:
            pass
        try:
            print("WINDOWS SHUTDOWN")
            os.system("shutdown /s /t 0")
        except:
            pass
    if type=='RESTART':
            try:
                os.system('sudo reboot')
            except:
                pass
            try:
                print("WINDOWS REBOOT")
                os.system("shutdown /r /t 0")
            except:
                pass