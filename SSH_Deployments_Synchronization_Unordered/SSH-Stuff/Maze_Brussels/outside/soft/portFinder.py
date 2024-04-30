from os import read
import re
import paho.mqtt.client as mqtt #import the client1
import time
import serial.tools.list_ports as port_list #port finder
import serial
from serial import SerialException
from serial.tools import list_ports
import configparser
from getTime import mytime 
from rpiConfiguration import makeConfiguration
from mqttConnection import *
from portFinder import *
import asyncio 

port="Unknown"

def findCom():
    while True:
        try:
            ports = list(port_list.comports())
            for port in ports:
                if port.manufacturer=="FTDI":
                    print(f"Arduino detected on com:{port.name}")
                    return port.name
            Arduino  = next(list_ports.grep("Nano"))
            print(f"Arduino detected on com: {Arduino.name} ") 
            return Arduino.name 
        except Exception as e:
            try:
                Arduino  = next(list_ports.grep("CH340"))
                print(f"Arduino detected on com: {Arduino.name} ") 
                return Arduino.name
            except Exception as e:
                try:
                    Arduino  = next(list_ports.grep("ACM0"))
                    Arduino.name='/dev/'+Arduino.name
                    print(f"Arduino detected on com: {Arduino.name} ") 
                    return Arduino.name
                except Exception as e:
                    try:
                        Arduino  = next(list_ports.grep("USB0"))
                        Arduino.name='/dev/'+Arduino.name
                        print(f"Arduino detected on com: {Arduino.name} ") 
                        return Arduino.name
                    except Exception as e:
                        try:
                            Arduino  = next(list_ports.grep("USB1"))
                            Arduino.name='/dev/'+Arduino.name
                            print(f"Arduino detected on com: {Arduino.name} ") 
                            return Arduino.name
                        except:
                            Arduino  = next(list_ports.grep("ACM1"))
                            Arduino.name='/dev/'+Arduino.name
                            print(f"Arduino detected on com: {Arduino.name} ") 
                            return Arduino.name


def makeConnection(port):
    global ser
    while True:
        try:
            ser=serial.Serial(port,baudrate=115200,timeout=0.1)
            print("-----Serial communication started-----")
            return ser
        except Exception as e:
            time.sleep(1)
            print("Trying to connect...")
            port=findCom()
            try:    
                ser=serial.Serial(port,baudrate=115200,timeout=1)
                print("Success...Arduino is now connected")
                return ser
            except Exception as e:
                time.sleep(1)    
