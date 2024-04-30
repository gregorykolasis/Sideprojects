import paho.mqtt.client as mqtt #import the client1
import time
############
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
    else:
        print(f"Bad connection Returned code: {rc}")
        client.bad_connection_flag=True
        #on_disconnect()
        

def on_disconnect(client, userdata, rc):
   print("Client disconnected")


########################################
mqtt.Client.connected_flag=False
mqtt.Client.bad_connection_flag=False 

broker_address="localhost"
print("creating new instance")
client = mqtt.Client("Arduino") #create new instance
########################################
client.on_message=on_message #attach functions to callback
client.on_disconnect = on_disconnect
client.on_connect=on_connect
#########################################
client.loop_start()
client.username_pw_set(username="mqtt",password="zagkoulis")


print("Connecting to broker",broker_address)
try:
    client.connect(broker_address) #connect to broker
except Exception as e:
    print(f"Connection failed. Error {e}")
    while True:
        print("Trying to connect...")
        try:
            client.connect(broker_address)
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
            client.connect(broker_address)
        except:
            print("Can't connect")



#client.loop_start() #start the loop
#print("Subscribing to topic","house/bulbs/bulb1")
#client.subscribe("house/bulbs/bulb1")
#print("Publishing message to topic","house/bulbs/bulb1")
#client.publish("house/bulbs/bulb1","OFF")
#time.sleep(4) # wait
#client.loop_stop() #stop the loop
while True:
    time.sleep(1)
    print("test")
