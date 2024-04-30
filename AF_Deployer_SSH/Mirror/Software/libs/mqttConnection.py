try:
    import paho.mqtt.client as mqtt
except ModuleNotFoundError as e:
    import os
    os.system("pip install paho-mqtt")
import time

global logger
logger = None

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

class myMQTT:
    def __init__(self , logger=None):
        self.logger = logger
        self.logger.debug('[MQTT]Init')
        
    client = None
    reconnectFlag = False

    def on_message(self,client, userdata, message):
        topic = message.topic
        msg = message.payload.decode('utf-8')
        qos = message.qos
        retain = message.retain;    
        client.messageCallback(topic,msg,qos,retain)
    
    def on_connect(self , client, userdata, flags, rc):
        if rc==0:
            self.logger.critical(f"[MQTT]Client connected with the Broker with code {rc}.")    
            self.setSubscription()
            self.client.connectedCallback()
        else:
            self.logger.error(f"[MQTT]Client bad connection Returned code: {rc}.")
        if self.reconnectFlag:
            self.reconnectFlag=False
            self.logger.critical("[MQTT]Client reconnected")


    def on_disconnect(self, client, userdata, rc):
        self.logger.error("[MQTT]Client disconnected")
        self.clientReconnect(rc)

    def clientReconnect(self,rc):
        global reconnectFlag
        reconnectFlag = True
        METHOD_RECONNECT = 1
        if METHOD_RECONNECT == 1:
            showMessages=True
            while rc != 0:
                if showMessages==True: self.logger.info("[MQTT]Reconnecting...")
                showMessages=False
                try:
                    time.sleep(1)
                    rc = self.client.reconnect()
                except Exception as e:
                    if self.client.onCannotConnect is not None: self.client.onCannotConnect(e)
        if METHOD_RECONNECT == 2:
            self.tryConnection()

    def clientInit(self,**kwargs):
        global logger

        self.logger.debug(f"[MQTT](clientInit) Args:{kwargs}")
        # requiredArgs = ['host']
        # for key, value in kwargs.items():
        #      if not key in requiredArgs:
        #          raise Exception(f"Sorry, but the required Args are :{requiredArgs}")
            
        self.port                = int(kwargs.get("port" , None))
        self.host                = kwargs.get("host" , None)
        self.username            = kwargs.get("username" , None)
        self.password            = kwargs.get("password" , '')
        self.uuid                = kwargs.get("uuid" , None)
        self.subscriptionTopics  = kwargs.get("topics" , [] )

        onMessage                = kwargs.get("onMessage" , None)
        onConnected              = kwargs.get("onConnected" , None)
        onCannotConnect          = kwargs.get("onCannotConnect" , None)

        kwargs['onConnected']
        kwargs['topics']
        kwargs['onMessage']

        self.logging             = kwargs.get("logging" , None )

        # for key, value in kwargs.items():
        #     if key=='host':

        if self.logging:
            logger = self.logging

        self.client = mqtt.Client(self.uuid,transport='websockets')
        self.client.connectedCallback  = onConnected
        self.client.messageCallback    = onMessage
        self.client.onCannotConnect    = onCannotConnect
  
        self.client.on_message         = self.on_message
        self.client.on_disconnect      = self.on_disconnect
        self.client.on_connect         = self.on_connect  
        if self.username:
            self.client.username_pw_set(
                username = self.username,
                password = self.password
            )   
        self.tryConnection()
        
    def setSubscription(self):
        self.logger.info("[MQTT]Setting subscriptions")
        self.logger.info(f"[MQTT]Topics:{self.subscriptionTopics}")
        self.client.subscribe(self.subscriptionTopics)

    def getClient(self):
        return self.client

    def tryConnection(self):
        showErrors = True
        self.logger.info(f"[MQTT-Connection]Connecting to broker:{self.host} port:{self.port}")
        while True: 
            try:        
                self.client.connect(self.host,self.port)
                self.client.loop_start()
                break
            except Exception as e:
                if self.client.onCannotConnect is not None: self.client.onCannotConnect(e)
                if showErrors : self.logger.error(f"[MQTT-Connection]Error:{e}")
                showErrors=False       
                try:       
                    self.client.connect(self.host,self.port)
                    self.client.loop_start()
                    break
                except:
                    time.sleep(2)

if __name__ == '__main__':
    instance = myMQTT()
    instance.clientInit(port=9001,host="localhost")