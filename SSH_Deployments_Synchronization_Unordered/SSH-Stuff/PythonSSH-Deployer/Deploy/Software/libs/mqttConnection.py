try:
    import paho.mqtt.client as mqtt
except ModuleNotFoundError as e:
    import os
    os.system("pip install paho-mqtt")

import time
from libs.configuration import getConfiguration,initConfiguration

global client,logger
client = 'Unknown'
logger = None

def printError(message):
    CRED = '\033[91m'
    CEND = '\033[0m'       
    msg = f"{CRED}{message}{CEND}"
    if logger: logger.info(msg)
    else: print(msg)

def printSuccess(message):
    CGREEN = '\033[32m'
    CEND = '\033[0m'       
    msg = f"{CGREEN}{message}{CEND}"
    if logger: logger.info(msg)
    else: print(msg)

def printGeneral(msg):
    if logger: logger.info(msg)
    else: print(msg)    

def on_message(client, userdata, message):
    topic = message.topic
    msg = message.payload.decode('utf-8')
    qos = message.qos
    retain = message.retain;    
    client.messageCallback(topic,msg,qos,retain)
  
def on_connect(client, userdata, flags, rc):
    if rc==0:
       printSuccess(f"[MQTT]Client connected with the Broker with code {rc}.")    
       setSubscription()
       client.connectedCallback()
    else:
       printError(f"[MQTT]Client bad connection Returned code: {rc}")

def clientReconnect(rc):
    METHOD_RECONNECT = 1
    if METHOD_RECONNECT == 1:
        showMessages=True
        while rc != 0:
            if showMessages==True: printGeneral("[MQTT]Reconnecting...")
            showMessages=False
            try:
                time.sleep(1)
                rc = client.reconnect()
            except Exception as e:
                pass
    if METHOD_RECONNECT == 2:
        tryConnection()

def on_disconnect(client, userdata, rc):
    printError("[MQTT]Client disconnected")
    clientReconnect(rc)

def clientInit(onMessageCallback,onConnectedCallback,topics,logging=None):
    global client,logger
    if logging:
        logger = logging
    initConfiguration()
    config = getConfiguration()   
    uuid = config["deviceId"]
    client = mqtt.Client(uuid,transport='websockets')
    
    client.connectedCallback = onConnectedCallback
    client.messageCallback = onMessageCallback
    client.subscriptionTopics = topics
    
    client.on_message    = on_message
    client.on_disconnect = on_disconnect
    client.on_connect    = on_connect  
    client.username_pw_set(
        username = config["username"],
        password = config["password"]
    )   
    tryConnection()
    
def match(sub, topic):
    if mqtt.topic_matches_sub(sub, topic)==False:
        #print("ERROR: "+sub+" "+topic)
        return False
    return True  

def getSinglewildcard(topic,IndexOfWildcard):
    readTopic = topic.split("/")
    nameTopic = readTopic[IndexOfWildcard]
    #printSuccess(f"[getSinglewildcard]{nameTopic}")
    return nameTopic
    
def setSubscription():
    global client
    printGeneral("[MQTT]Setting subscriptions")
    printGeneral(f"[MQTT]Topics:{client.subscriptionTopics}")
    client.subscribe(client.subscriptionTopics)

def getClient():
    return client

def tryConnection():
    showErrors = True
    config = getConfiguration()   
    broker = config["host"]
    port   = int(config["port"])  
    printGeneral(f"[MQTT-Connection]Connecting to broker:{broker} port:{port}")
    while True: 
        try:        
            client.connect(broker,port)
            client.loop_start()
            break
        except Exception as e:
            if showErrors : printError(f"[MQTT-Connection]Error:{e}")
            showErrors=False       
            try:       
                client.connect(broker,port)
                client.loop_start()
                break
            except:
                time.sleep(2)