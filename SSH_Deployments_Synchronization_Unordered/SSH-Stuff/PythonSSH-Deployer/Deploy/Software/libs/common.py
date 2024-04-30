import socket
from time import time
from time import sleep
from random import *

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


