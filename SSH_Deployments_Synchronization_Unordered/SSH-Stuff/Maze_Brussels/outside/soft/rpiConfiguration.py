import configparser
from getip import getip
from uuid import uuid4
from __main__ import *
import os


def makeConfiguration():
    config = configparser.ConfigParser(strict=False)
    defPath = os.path.abspath(os.path.join(__file__, "../"))
    default_filename = f"{defPath}/config.ini"   
    print(f"path Configuration-->{default_filename}")
    config.read(default_filename)
    if 'ID'in config:
        print("Configuration is already completed")
    else:
        config.add_section('ID')
        config.set("ID",'ipAddress',f"{getip()}")
        config.set('ID','deviceId',f"{str(uuid4())}")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
            print("Configuration completed")
    config.sections()
    host=config['CONNECTION']['host']
    port=config['CONNECTION']['port']
    username=config['CONNECTION']['username']
    password=config['CONNECTION']['password']
    startup=config['TOPICS']['startup']
    roomName=config['ROOM']['roomName']
    deviceType=config['ROOM']['devicetype']
    ipAddress=config['ID']['ipaddress']
    deviceId=config['ID']['deviceid']
    print("Parser:OK")
    return host,port,username,password,startup,roomName,deviceType,ipAddress,deviceId

