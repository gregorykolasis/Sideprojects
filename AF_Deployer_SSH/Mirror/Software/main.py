import asyncio
import datetime
import json
import os
from operator import itemgetter as objParser
from threading import Timer
from time import sleep
from uuid import uuid4
import subprocess
import logging
import random

path = os.path.abspath(os.path.join(__file__, "../")); config = f"{path}/config.ini" 
from libs.configuration import getConfiguration, initConfiguration
initConfiguration(config)  

from libs.enums import EVENTS, PROJECT, ROOMSTATE
from libs.utils import myTimestamp, myIP , myMAC , powerOff , restartScript , getPlatform
from libs.myGameplay import myGameplay
from libs.myLogger import setLogger
from libs.myMusic import myMusic
from libs.myWS import myWS
from libs.mqttConnection import myMQTT , match, getSinglewildcard
from libs.mySerial import mySerial

CITY = 'dorsten' #'dorsten'
USE_SERIAL_GAME = False

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
    imported = __import__(f"rooms.{CITY}.{objParser('roomName')(getConfiguration())}", fromlist=['myGamecontrol'])   
    Gameplay = getattr(imported, 'myGamecontrol')  
    extraClass = classFactory(Gameplay)
except Exception as e:
    extraClass = classFactory(emptyClass)

class myMain( myGameplay, myMusic , extraClass , myWS ,  mySerial ,):

    def __init__(self, loop=None):
        self.loop = loop  
        #self.myMethods()
        self.mainLoop()
              
    DEBUG_TIMERS = False
    SESSION_LOGGING = False
    PROJECT = PROJECT.AF
    DEV = False

    difficulty = 'UNKNOWN'

    def setupLogger(self,loggingType):
        # myLogger.__init__(self)  
        if self.SESSION_LOGGING:
            now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            date = datetime.datetime.now().strftime('%Y_%m_%d')
            subFolder = f"{self.roomName}_Session_{date}"
            subFolderPath = f"{path}/logs/{subFolder}"
            isExist = os.path.exists(subFolderPath)
            if not isExist:
                os.makedirs(subFolderPath)
            filename = f"{subFolderPath}/{self.roomName}_{now}.log" 
        else:
            filename = f"{path}/logs/{self.roomName}.log"  
        if self.SESSION_LOGGING: self.logger.info('[Main]This script is using SESSION_LOGGING')   
        setLogger(filename,loggingType)
        self.logger = logging.getLogger()

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
                self.doorTimer = Timer(1,self.sendMQTT,[EVENTS.DOORCLOSED])
                self.doorTimer.start() 
            elif topic==self.reset:
                self.logger.info("[State]==================RESET==========================")
                self.gameControl("reset")
            elif topic==self.settings:
                self.logger.info("[State]==================SETTINGS=======================")
                self.makeId(msg)
                self.gameControl("settings",msg)
            elif topic==self.panicTopic:
                self.logger.info("[State]==================PANICBUTTON====================")
                self.gameControl("panic")             
                self.playPanic()
            elif topic==self.restartedserver:
                randomDelays = [1,2,3,4,5,6,7,8,9,10]
                sleep(random.choice(randomDelays))
                restartScript()
            elif topic==self.controlpower:
                data = json.loads(msg)
                powerOff(data["action"])
            else:
                try:
                    self.customConsume(data) #Anything else maybe be adopted by customGame-Scenario
                except Exception as e:
                    pass
                
        except Exception as e:
            print(e)       

    def openUI(self):

        thridScreenPath = None
        host = objParser('host')(getConfiguration())
        showPoints = "false"

        roomsWithPoints = ['alleyoops','highlightbars','goal','spacejam','funinthebarn','thegulf','thepitcher','thegulf']
        if self.roomName in roomsWithPoints:
            showPoints = "true"

        if getPlatform()=='linux':
            browser = "/usr/bin/chromium"
            killBrowser = "pkill chromium"
        else:
            browser = "start chrome.exe"
            killBrowser = "taskkill /F /IM chrome.exe /T > nul"  

        killExistingChromium = subprocess.Popen(killBrowser,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        killExistingChromium.wait()

        disableCache = '--incognito'

        ratio = 1920
        setOrientation = {
            "inside":ratio*0,
            "outside":ratio*1,
            "third":ratio*2
        }
        windowPosInside  = f"{setOrientation['inside']},0"
        windowPosOutside = f"{setOrientation['outside']},0"
        windowPosThird   = f"{setOrientation['third']},0"
        try:
            f = open(f'{path}/orientation/{CITY}/orientation.json')
            data = json.load(f)
            if self.roomName in data:     
                orientationArray = data[self.roomName]
                self.logger.warning(orientationArray)
                for i,v in enumerate(orientationArray):
                    setOrientation[v] = i*ratio
                self.logger.warning(f"New-Orientation:{setOrientation}")
                windowPosInside  = f"{setOrientation['inside']},0"
                windowPosOutside = f"{setOrientation['outside']},0"
                windowPosThird   = f"{setOrientation['third']},0"
            else:
                self.logger.error(f"[Orientation] Doesn't exist for {self.roomName} Loading Defaults:{setOrientation}")
        except Exception as e:
            self.logger.error(f"[Orientation] Tried to load it , got Error:{e} Propably:{self.roomName} in orientation.json , isn't an array or orientation.json file has errors")  


        typeScreen = 'inside'
        url = f"{host}/{typeScreen}/{self.roomName}?showPoints={showPoints}"
        args = f'--app="http://{url}" --window-position={windowPosInside} --user-data-dir=c:/chrome/{typeScreen} {disableCache}'
        kiosk = ''
        #kiosk = '--kiosk'
        kiosk = '--start-fullscreen'
        completedPath = f'''{browser} {kiosk} {args}'''
        print(completedPath)
        openChromium = subprocess.Popen(completedPath,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        if self.PROJECT==PROJECT.AF or self.DEV:
            typeScreen = 'outside'
            
            url = f"{host}/{typeScreen}/{self.roomName}"
            args = f'--app="http://{url}" --window-position={windowPosOutside} --user-data-dir=c:/chrome/{typeScreen} {disableCache}'

            kiosk = ''
            #kiosk = '--kiosk'
            kiosk = '--start-fullscreen'
            completedPath = f'''{browser} {kiosk} {args}'''
            print(completedPath)
            openChromium = subprocess.Popen(completedPath,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

        try:
            f = open(f'{path}/screens.json')
            data = json.load(f)
            if self.roomName in data:     
                thridScreenPath = data[self.roomName]
                print(thridScreenPath)
            else:
                self.logger.info(f"[3rdScreen] Doesn't exist for {self.roomName}")
        except Exception as e:
            self.logger.info(f"[3rdScreen] Tried to load 3rd Screen , got Error:{e}")    
    
        if thridScreenPath != None:
            if self.DEV:
                thridScreenPath = str(thridScreenPath).replace("IE/thirdScreen","laragon/www")
                print(thridScreenPath)      
            pathScreen = thridScreenPath.replace('''file:///''',"") 
            screenExists = os.path.exists(pathScreen)
            if not screenExists:
                self.logger.warning("[3rdScreen] This room has assigned 3rd Screen , but can't find the files")           
            if screenExists:
                typeScreen = 'thirdscreen'
                url = thridScreenPath
                useHttp = "http://"
                if 'file' in thridScreenPath:
                    useHttp = ''
                args = f'--app="{useHttp}{url}" --window-position={windowPosThird} --user-data-dir=c:/chrome/{typeScreen} {disableCache}'
                kiosk = ''
                #kiosk = '--kiosk'
                kiosk = '--start-fullscreen'
                completedPath = f'''{browser} {kiosk} {args}'''
                print(completedPath)
                openChromium = subprocess.Popen(completedPath,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            
    def connectedCallback(self):
        msg = {
            "timestamp"  : myTimestamp(),
            "ipAddress"  : myIP(),
            "deviceId"   : self.deviceId,
            "macAddress" : myMAC(),
            "roomName"   : self.roomName,
            "deviceType" : self.deviceType
        }
        self.publish(self.startup,json.dumps(msg))
        sleep(1)
        if self.PROJECT == PROJECT.AF and not self.DEV:
            self.scannerId = f"{self.roomName}Scanner_{str(uuid4())[:6]}"
            self.client.subscribe(f"/themaze/booted/{self.scannerId}",0)
            msg = {
                "timestamp"  : myTimestamp(),
                "ipAddress"  : myIP(),
                "deviceId"   : self.scannerId,
                "macAddress" : myMAC(),
                "roomName"   : self.roomName,
                "deviceType" : "RPI_READER"
            }
            self.publish(self.startup,json.dumps(msg))
        if not self.DEV:
            self.openUI()     
        try:
            self.customSubscribe()
        except Exception as e:
            pass
        
    def scanOutside(self,rfid):
        TopicWristbandScan = f"/themaze/{self.scannerId}/rpi/wristbandScan"
        rfid = rfid.replace("[Outside]Rfid:","")
        rfid  = str(rfid)
        color = int(rfid[0])
        id    = int(rfid[1:])
        self.playScan()
        msg = { "timestamp" : myTimestamp(), "wristbandNumber": id, "wristbandColor": color }
        print(msg)
        self.publish(f"{TopicWristbandScan}",json.dumps(msg)) 

    def specialButtons(self,data):
        self.logger.info(f"[specialButtons]Raw:{data}")
        specialWords = ['Button_Diff_EASY','Button_Diff_MEDIUM','Button_Diff_HARD','Button_Inside_LANG','Button_Outside_LANG','Button_Game_PANIC']
        valid = False
        for x in specialWords:
            if x == data:
                valid=True
        if valid:
            if "Diff" in data:
                diff = data.replace("Button_Diff_","")
                self.logger.info(f"[Buttons-Game]Choose difficulty pressed ROOMSTATE:{self.roomState} REGAME:{self.enableRegame}")        
                if self.roomState == ROOMSTATE.TEAMREGISTER:
                    waitInside = False
                    try:
                        if self.doorTimer.is_alive():
                            waitInside = True
                    except:
                        pass
                    if not waitInside:
                        msg = {"timestamp": myTimestamp() , "gameId": self.gameId, "difficulty": diff}     
                        self.publish(self.choosedifficulty,json.dumps(msg))
                    else:
                        self.logger.warning("Waiting for inside Screeen")
                elif self.roomState == ROOMSTATE.STANDBY and self.enableRegame:
                    msg = {"timestamp": myTimestamp() , "teamName": self.teamName, "difficulty": diff}     
                    self.publish(self.regame,json.dumps(msg))  
            if "PANIC" in data :#and (self.roomState == ROOMSTATE.PLAYING or self.roomState==ROOMSTATE.STANDBY):
                self.logger.info("[Buttons-Game]PANIC pressed")
                diff = data.replace("Button_Game_","")           
                msg = {"timestamp": myTimestamp() , "gameId": self.gameId}     
                self.publish(self.panic,json.dumps(msg))
            if "LANG" in data:  
                self.logger.info("[Buttons-Game]Change langued pressed")           
                msg = {"timestamp": myTimestamp()}     
                self.publish(self.changeLanguage,json.dumps(msg))               

    def mqttCannotconnect(self, e):
        pass

    def mainLoop(self):        
        try:
            self.setupLogger(logging.INFO)
            myGameplay.__init__(self, self.loop)
            myMusic.__init__(self)    
            if USE_SERIAL_GAME:
                mySerial.__init__(self, self.loop)      
                self.sendSerial = self.serialSend
            else:
                myWS.__init__(self, self.loop)        
                self.startWS()
            try:
                extraClass.__init__(self,self.loop) 
            except Exception as e:
                self.logger.info(f"[Exception]Extra class:{e}")       
                self.logger.error(f"[Init]{self.roomName} has errors or doesn't exist in City:{CITY}")         
        except Exception as e:
            print(e)

        self.panicTopic = ''
        if self.PROJECT==PROJECT.AF:
            self.panicTopic=f"{self.panic}/response"
        else:
            self.DEV = False
            self.oldFileSystem = True
            self.panicTopic=self.panic  

        topics = [
          (self.init,0),
          (self.reset,0),
          (self.settings,0),
          (self.panicTopic,0),
          (f"/themaze/booted/{self.deviceId}",0),
          (self.restartedserver,0),
          (self.controlpower,0)
        ]

        host, port, uuid ,username, password = objParser('host','port','deviceId','username','password')(getConfiguration())    
        MQTT = myMQTT(self.logger)
        MQTT.clientInit(  
            host = host, port = port, uuid = uuid, username = username, password = password,
            onMessage = self.consumeMessage,        
            onConnected = self.connectedCallback, 
            onCannotConnect = self.mqttCannotconnect,
            topics = topics,     
            logger = self.logger
        )       
        self.client = MQTT.getClient()      
        try:
            self.loop.run_forever()         
        except Exception as e:
            print(f'[myMain] Error {e}')
        finally:
            print(f'[myMain] Error Finally')
            self.loop.close()

loop = asyncio.get_event_loop()
theMain = myMain(loop)