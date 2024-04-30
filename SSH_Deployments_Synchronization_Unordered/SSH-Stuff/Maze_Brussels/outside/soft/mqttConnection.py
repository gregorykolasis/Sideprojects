import paho.mqtt.client as mqtt #import the client1
import time
from getTime import mytime 
from rpiConfiguration import makeConfiguration
import asyncio
import json
host,port,username,password,startup,roomName,deviceType,ipAddress,deviceId=makeConfiguration()

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

def on_connect(client, userdata, flags, rc):
    if rc==0:
       client.connected_flag=True #set flag
       print (f"Client connected with the Broker with code {rc}.")
       client.bad_connection_flag=False
       msg = 	{
			"timestamp" : mytime(),
	#		"ipAddress": ipAddress,
			"deviceId": deviceId,
			"roomName": roomName,
			"deviceType": deviceType
		    }
       msg= json.dumps(msg)
       client.publish("/themaze/booted", msg, qos=2)
       print("Init message sent")
    else:
        print(f"Bad connection Returned code: {rc}")
        client.bad_connection_flag=True
        #on_disconnect()
    
        
def on_disconnect(client, userdata, rc):
   print("Client disconnected")
   client.connected_flag=False

########################################
def MQTTconfig():
    mqtt.Client.connected_flag=False
    mqtt.Client.bad_connection_flag=False 
    print("Creating new instance")
    client = mqtt.Client(roomName) #create new instance 
    ########################################
    client.on_message=on_message #attach functions to callback
    client.on_disconnect = on_disconnect
    client.on_connect=on_connect
    #########################################
    client.loop_start()
    client.username_pw_set(username=username,password=password)
    print("Connecting to broker:",host)

    try:
        client.connect(host) #connect to broker
    except Exception as e:
        print(f"Connection failed. Error {e}")
        while True:
            print("Trying to connect...")
            try:
                client.connect(host)
                break
            except Exception as e:
                print(f"Connection failed. Error {e}")
            
    while not client.connected_flag: #wait in loop
        print("Waiting for client connected flag")
        time.sleep(1)

    if client.bad_connection_flag:
        while client.bad.connected_flag:
            print("Trying to connect. bad connected flag")
            try:
                client.connect(host)
            except:
                print("Can't connect")

    subscriber=startup+"/"+deviceId+"/#"
   # subscriber=startup+"/#"  
    print(subscriber)
    client.subscribe(subscriber)
    print(f"connected:{client.connected_flag}")
    return client
###MQTTT

