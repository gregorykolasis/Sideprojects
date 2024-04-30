import asyncio
import datetime
import json
import os
import re
from operator import itemgetter as objParser
from threading import Timer
from time import sleep
from uuid import uuid4

from libs.configuration import getConfiguration, initConfiguration
from libs.enums import EVENTS, PROJECT, ROOMSTATE
from libs.common import myTimestamp, myIP
from libs.myGameplay import myGameplay
from libs.myLogger import myLogger
from libs.myMusic import myMusic
from libs.myWS import myWS
from libs.mqttConnection import clientInit, getClient, match, getSinglewildcard


class emptyClass():
    def __init__(self, loop):
        self.loop = loop
        object.__init__(loop)

def classFactory(object):
    class myClass(object):
        def __init__(self, loop):
            self.loop = loop
            object.__init__(loop)
    return myClass

try:
    imported = __import__(f"rooms.{objParser('roomName')(getConfiguration())}", fromlist=['myGamecontrol'])   
    Gameplay = getattr(imported, 'myGamecontrol')  
    extraClass = classFactory(Gameplay)
except Exception as e:
    extraClass = classFactory(emptyClass)

class myMain( myGameplay, myWS, myLogger, myMusic , extraClass ):

    def __init__(self, loop=None):
        self.loop = loop  
        #self.myMethods()
        self.mainLoop()
              
    DEBUG_TIMERS = False
    SESSION_LOGGING = True
    PROJECT = PROJECT.MAZE

    def myMethods(self):
        allMethods = [method for method in dir(
            myMain) if method.startswith('__') is False]
        print(allMethods)

    def publish(self,topic,message,retained=False):
        self.logger.info(f"[MQTT-Send-Topic]:{topic}")
        self.logger.info(f"[MQTT-Send-Data]:{message}")
        self.client.publish(topic,message,qos=2,retain=retained)        
              
    def consumeMessage(self,topic,msg,gos,retain): 
        self.logger.info(f"[MQTT-Receive-Topic]:{topic}")
        self.logger.info(f"[MQTT-Receive-Data]:{msg}")
        try:
            if topic==self.init:
                self.logger.info("[State]==================TEAM-REGISTER==================")
                self.makeId(msg)
                self.gameControl("teamRegister")          
                self.logger.info("Sending default message doorClosed...")
                doorTimer = Timer(0.5,self.sendMQTT,[EVENTS.DOORCLOSED])
                doorTimer.start() 
            if topic==self.reset:
                self.logger.info("[State]==================RESET==========================")
                self.gameControl("reset")
            if topic==self.settings:
                self.logger.info("[State]==================SETTINGS=======================")
                self.makeId(msg)
                self.gameControl("settings",msg)
            if topic==f"{self.panic}/response":
                self.logger.info("[State]==================PANICBUTTON====================")
                self.gameControl("panic")
        except Exception as e:
            print(e)       

    def connectedCallback(self):
        msg = {
            "timestamp" : myTimestamp(),
            "ipAddress" : myIP(),
            "deviceId"  : self.deviceId,
            "roomName"  : self.roomName,
            "deviceType": self.deviceType
        }
        self.publish(self.startup,json.dumps(msg))
        sleep(1)
        if self.PROJECT == PROJECT.AF:
            self.scannerId = f"{self.roomName}Scanner_{str(uuid4())[:6]}"
            self.client.subscribe(f"/themaze/booted/{self.scannerId}",0)
            msg = {
                "timestamp" : myTimestamp(),
                "ipAddress" : myIP(),
                "deviceId"  : self.scannerId,
                "roomName"  : self.roomName,
                "deviceType": "RPI_READER"
            }
            self.publish(self.startup,json.dumps(msg))      

    def scanOutside(self,rfid):
        TopicWristbandScan = f"/themaze/{self.scannerId}/rpi/wristbandScan"
        color = rfid[-1]
        id = rfid[:-1]
        id = id.replace("[Outside]Rfid:","")
        msg = { "timestamp" : myTimestamp(), "wristbandNumber": id, "wristbandColor": color }
        print(msg)
        self.publish(f"{TopicWristbandScan}",json.dumps(msg)) 

    def specialButtons(self,data):
        specialWords = ['Button_Diff_EASY','Button_Diff_MEDIUM','Button_Diff_HARD','Button_Inside_LANG','Button_Outside_LANG','Button_Game_PANIC']
        valid = False
        for x in specialWords:
            if x == data:
                valid=True
        if valid:
            if "Diff" in data:
                diff = data.replace("Button_Diff_","")           
                if self.roomState == ROOMSTATE.RESET:      
                    msg = {"timestamp": myTimestamp() , "gameId": self.gameId, "difficulty": diff}     
                    self.publish(self.choosedifficulty,json.dumps(msg))  
                elif self.roomState == ROOMSTATE.STANDBY and self.enableRegame:
                    msg = {"timestamp": myTimestamp() , "teamName": self.teamName, "difficulty": diff}     
                    self.publish(self.regame,json.dumps(msg))  
            if "PANIC" in data and self.roomState == ROOMSTATE.PLAYING or self.roomState==ROOMSTATE.STANDBY:
                diff = data.replace("Button_Game_","")           
                msg = {"timestamp": myTimestamp() , "gameId": self.gameId}     
                self.publish(self.panic,json.dumps(msg))
            if "LANG" in data:  
                msg = {"timestamp": myTimestamp()}     
                self.publish(self.changeLanguage,json.dumps(msg))               

    def mainLoop(self):        
        try:
            myLogger.__init__(self) 

            path = os.path.abspath(os.path.join(__file__, "../")); 
            if self.SESSION_LOGGING:
                now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                date = datetime.datetime.now().strftime('%Y_%m_%d')
                subFolder = f"{self.roomName}_Session_{date}"
                subFolderPath = f"{path}/logs/{subFolder}"
                isExist = os.path.exists(subFolderPath)
                if not isExist:
                    os.makedirs(subFolderPath)
                filename = f"{subFolderPath}/{self.roomName}_{now}.txt" 
            else:
                filename = f"{path}/logs/{self.roomName}.txt"  
            self.initLogger(filename)   
            myGameplay.__init__(self, self.loop)
            myWS.__init__(self, self.loop)        
            myMusic.__init__(self)    
            self.startWS()
            if self.SESSION_LOGGING: self.logger.info('[Main]This script is using SESSION_LOGGING')   
            try:
                extraClass.__init__(self,self.loop)    
            except Exception as e:
                self.logger.info(f"[Exception]Extra class:{e}")
            
        except Exception as e:
            print(e)

        topics = [
          (self.init,0),
          (self.reset,0),
          (self.settings,0),
          (f"{self.panic}/response",0),
          (f"/themaze/booted/{self.deviceId}",0),
        ]

        clientInit(self.consumeMessage,self.connectedCallback,topics,self.logger)       
        self.client = getClient()      
        try:
            self.loop.run_forever()         
        except Exception as e:
            print(f'[myMain] Error {e}')
        finally:
            print(f'[myMain] Error Finally')
            self.loop.close()

loop = asyncio.get_event_loop()
theMain = myMain(loop)