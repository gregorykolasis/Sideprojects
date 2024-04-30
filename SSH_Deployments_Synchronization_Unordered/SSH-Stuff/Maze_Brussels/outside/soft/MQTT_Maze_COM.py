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
import json

#time.sleep(10)

#Parser
host,port,username,password,startup,roomName,deviceType,ipAddress,deviceId=makeConfiguration()
###MQTT
client=MQTTconfig()
global arduinoConnected
arduinoConnected=False
try:
    port=findCom()
    print(f"Port:{port}")
    ser=makeConnection(port)
except Exception as e:
    print("Serial communication failed,28 error {e}")
    time.sleep(1)
    print("Trying to connect...")
    while True:
        try:
            port=findCom()
            ser=makeConnection(port)
            break
        except Exception as e:
            print(f"Can't create connection,37 error {e}")
            time.sleep(1)    

def doRead():
    tic     = time.time()
    buff    = ""
    # you can use if not ('\n' in buff) too if you don't like re
    while ((time.time() - tic) <= 1):
        #print(time.time() - tic)
        c = ser.read(1)
        buff += c.decode("utf-8","ignore").rstrip()
    return buff

while True:    
    try:
        if ser.is_open and arduinoConnected==False:
            connectionmsg={
                "timestamp":mytime(),
                "connectionStatus":"connected"
            }
          #  client.publish(f"/themaze/{deviceId}/rpi/connection",f"{connectionmsg}",qos=2)
            arduinoConnected=True

        if ser.in_waiting>0:
            #read_serial=ser.readline().decode('utf-8').rstrip()
            read_serial = doRead()
            print(f"Message from Arduino: {read_serial}")
            if "Error" in read_serial:
                print("Error")
            elif "RFID" in read_serial:
                pass
            elif len(read_serial)>1:
                rfidId=read_serial[:-1]
                rfidColor=read_serial[-1:]
                print(f"rfidId:{rfidId}")
                print(f"rfidColor:{rfidColor}")      
                msg=    {
	                      "timestamp" : mytime(), 
                          "wristbandNumber": rfidId,
	                      "wristbandColor": rfidColor
                         }
                msg= json.dumps(msg)
                client.publish(f"/themaze/{deviceId}/rpi/wristbandScan",msg,qos=2)

    except Exception as e:
        connectionmsg={
                "timestamp":mytime(),
                "connectionStatus":"disconnected"
            }
     #   client.publish(f"/themaze/{deviceId}/rpi/connection",f"{connectionmsg}",qos=2)
        arduinoConnected=False
        print(f"Serial communication stopped,74 error {e}")
        time.sleep(1)
        print(f"Serial state: {ser.is_open}")
        if ser.is_open:
            print("Ser is closing...")
            ser.close()
        print("Trying to reconnect...")       
        while True:
            try:
                port=findCom()
                ser.port=port
                ser.open()
                print("Success...Arduinos are now connected")
                break
            except Exception as e:
                print(f"Can't create connection,89 error {e}")
                time.sleep(1)
  


        



    
