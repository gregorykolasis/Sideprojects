from libs.configuration import getConfiguration,initConfiguration
from libs.common import search,myTimestamp
from operator import itemgetter as objParser
import json
from threading import Timer
from libs.enums import EVENTS,ROOMSTATE,ROOMTYPE
import re

class myGameplay:
    def __init__(self, loop=None):
        self.loop = loop

    initConfiguration()

    gamePlaying=False; gameId=0; score=0; subRound=0; players=0; roundCounter=0; rounds=0

    wristbandNumber=0; final=0; finalStarted=0; 
    
    finalTimer=0; 
    countdownTimer=0; 
    gameTimer=0; 
    timeGame=0; 
    startTime=0
    enableRegameTimer=0
    enableRegame=False

    startup,booted,init,reset,doorClosed,settings,scored,end,regame,error,panic,choosedifficulty,changeLanguage = objParser('startup',
    'booted','init','reset','doorClosed','settings','scored','end','regame','error','panic','choosedifficulty','changeLanguage')(getConfiguration())      
    
    roomName,final,finalRole = objParser('roomName','final','finalRole')(getConfiguration())      
    
    deviceType,deviceId = objParser('deviceType','deviceId')(getConfiguration())        

    waitCheckflag=False; difficulty='Unknown'

    def sendSCREEN(self,msg="Unknown"):
        topicName="Unknown"
        if self.roomName=="letterfloor":
            topicName="lettergame"
        if self.roomName=="joker":
            topicName="jokergame"      
        msg= json.dumps(msg)
        self.publish(f"{topicName}/screen",msg,retained=True)

    def sendMQTT(self,event,data="Unknown"):
        if event == EVENTS.DOORCLOSED:
            msg = { "timestamp": myTimestamp(), "gameId":self.gameId }
            msg = json.dumps(msg)
            self.publish(self.doorClosed,msg)
        elif event == EVENTS.WIN or event == EVENTS.LOSE or event == EVENTS.PANICBUTTON:
            timeSpent = (myTimestamp() - self.startTime)/1000
            timeSpent = round(timeSpent,0)
            timeSpent = int(timeSpent)
            timeLeft  = self.timeGame-timeSpent
            msg = { "timestamp":myTimestamp(), "gameId":self.gameId, "reason":event, "timeAllocated":self.timeGame, "timeSpent":timeSpent,  "timeLeft":timeLeft }    
            self.publish(self.end,json.dumps(msg))      
        elif event == EVENTS.SCORED:
            msg = { "timestamp":myTimestamp(), "sensorName":data, "remainingScore":self.score, "gameId":self.gameId}  
            self.publish(self.scored,json.dumps(msg))    

    def roomInit(self):    
        self.gamePlaying     = False
        self.finalStarted    = False
        self.gameId          = None
        self.wristbandNumber = 0
        self.timeGame        = 0
        self.rounds          = 0
        self.logger.info("[Room]=================Initialiazation is completed/First time booted===================")

    def makeId(self,msg):
        msg = json.loads(msg)
        self.gameId = msg['gameId']
        self.logger.info(f"[Game]GameID:{self.gameId}")    

    def gameEnded(self,result):
        self.gamePlaying=False
        self.logger.info(f"[Game]==================================FINISHED:{result}==================================")
        self.sendMQTT(result)
        self.stopMusic()
        if result == EVENTS.WIN:
            self.winSound()     
        if result == EVENTS.LOSE:
            self.failSound()        
        self.standbyMode()

    def checkSimplescore(self,msg):
        if re.search(r"sensor[0-9]+", msg):
            self.score=self.score-1
            if self.score==0:
                self.gameEnded(EVENTS.WIN)
            else:
                self.soundScored()
                print(f"Score:{self.score}")
                self.sendMQTT(EVENTS.SCORED,msg) 

    def check1SensorLose(self,msg):
        if re.search(r"sensor[0-9]+", msg) or ('lightsensor' in msg and 'off' in msg):                
            self.logger.info(f"[Gameplay]Sensor trigger with name:{msg}")
            self.score+=1
            loseGame = True       
            if self.roomName=='laserdance': 
                if self.waitCheckflag==False:
                    loseGame=False
                    self.score+=-1
                    self.logger.info(f"[Gameplay]IGNORE sensor trigger with name:{msg}")    
            if loseGame and self.roomName == 'laserdance':
                maxFails=3
                if self.difficulty=="MEDIUM": maxFails=2
                if self.difficulty=="HARD":   maxFails=1
                if self.difficulty=="EASY":   maxFails=3
                self.logger.info(f"[Gameplay]====Fail Attempts:{self.score}/{maxFails}")
                if self.score < maxFails:          
                    loseGame=False               
            if loseGame:
                self.gameEnded(EVENTS.LOSE)

    def checkRoom(self,msg):
        r = self.roomName
        if r==ROOMTYPE.ALLEYOOPS or r==ROOMTYPE.SPACEJAM or r==ROOMTYPE.GOAL:
            self.checkSimplescore(msg)  #Win if you score the points
        elif r==ROOMTYPE.JUSTDOIT or r==ROOMTYPE.SUCKERPUNCH or r==ROOMTYPE.LASERDANCE:
            self.check1SensorLose(msg)  #Lose if 1 Sensors is triggered        
        elif r==ROOMTYPE.REFLECTIONS or r==ROOMTYPE.BUBBLEBOBBLE or r==ROOMTYPE.GRANDPIANO or r==ROOMTYPE.LETTERFLOOR or r==ROOMTYPE.FUNINTHEBARN:
            self.checkGameCustom(msg)

    def checkSerial(self,msg):       
        if msg =="doorClosed":
            self.sendMQTT(EVENTS.DOORCLOSED)
        elif msg =="doorOpened":
            self.sendMQTT(EVENTS.DOOROPENED)
        elif self.gamePlaying:
            self.checkRoom(msg)
        if self.finalStarted and self.gamePlaying:  
            if msg=="redScan" or msg=="purpleScan" or msg=="greenScan" or msg=="yellowScan" or msg=="blueScan" or msg=="orangeScan":
                self.wristbandNumber-=1
                self.playsound("pressed")
                self.logger.info(f"[Gameplay]Length of Wristbands to be scanned:{self.wristbandNumber}")
            if self.wristbandNumber==0:
                self.gameEnded(EVENTS.WIN)

    def gameStart(self,gameConfiguration):
        if self.gamePlaying==False:
            self.roomState = ROOMSTATE.PLAYING
            self.gamePlaying=True
            self.getGameConfiguration(gameConfiguration)        
            self.stopMusic()
            self.startMusic() 
            self.sendSerial("openLights")     
            self.sendSerial("start")   
            self.startTimers()            
            try:
                self.startGameCustom()
            except Exception as e:
                self.logger.info("[gameStart]Not Custom Game here") 
            self.logger.info("[Room]==============GAME-GOT-CONFIGURATION-IS-STARTING==============")
        else:
            self.logger.info("[gameStart]Game has already started")

    def gameControl(self,state,data='Unknown'):
        if state == "teamRegister":
            self.stopMusic()
            self.startMusic()
            self.sendSerial("openLights")
            self.sendSerial("openDoor")
            self.sendSerial("checkDoor")
        elif state == "reset":
            self.resetRoom()
        elif state == "panic":
            self.sendMQTT("PANICBUTTON")        
            self.resetRoom()
        elif state == "settings":
            if not self.IsMasterConnected():
                self.logger.error('[Gameplay]Game gonna start , but MASTER Is not connected!')
            self.gameStart(data)
        
    def customGameStandby(self):
        r = self.roomName
        if r==ROOMTYPE.REFLECTIONS or r==ROOMTYPE.LASERDANCE:
            self.resetLasers()
            if r==ROOMTYPE.LASERDANCE: 
                self.disableChecklaserdance()

    def standbyMode(self): #Awaiting to check difficulty
        self.lockRegame()
        self.roomState = ROOMSTATE.STANDBY
        self.gamePlaying=False  
        self.sendSerial("stop")
        #sendSerial("openDoor")
        self.resetTimers()
        self.score=0
        self.wristbandNumber=0
        self.timeGame=0
        try:
            self.standbyGameCustom()
        except Exception as e:
            self.logger.warning(f"[standbyGameCustom] not Exist")
        self.customGameStandby()
        if self.final==True:
            print("Reset Final")
            self.resetFinal()
        self.logger.info("[Room]==============STANDBY==============")       

    def resetRoom(self):
        self.roomState = ROOMSTATE.RESET
        self.gamePlaying=False
        self.sendSerial("stop")
        self.sendSerial("openDoor")
        self.sendSerial("closeLights")  
        self.stopMusic()
        self.resetTimers()  
        if self.roomName=="laserdance":
            self.disableChecklaserdance()     
        if self.roomName=="letterfloor":
            msg = {"word":" ","nextletter":0,"gameStatus":"LOSE"}
            self.sendSCREEN(msg)    
        if self.final==True:
            self.resetFinal()  
        self.score=0
        self.wristbandNumber=0
        self.timeGame=0
        self.players=0
        self.resetGameCustom()
        self.logger.info("[Room]==============RESET==============")  

    def getGameConfiguration(self,configuration):

        configuration = json.loads(configuration)
        self.wristbands = [configuration['playersWristbandsList'][wrist]['wristbandColor'] for wrist,x in enumerate (configuration['playersWristbandsList'])]
        self.players = len(self.wristbands)
        self.wristbands = (','.join(map(str,self.wristbands)))
        
        if self.players>6: 
            self.logger.warning(f"[Bug]Players appeared to be greater than 6 epsecially:{self.players} will be adjusted to max Value:6")
            self.players = 6 

        self.logger.info(f"[Game-Configuration]Players:{self.players}")  
        self.logger.info(f"[Game-Configuration]Wristbands:{self.wristbands}")  

        try:
            self.score = configuration['pointsToWin']
            self.logger.info(f"[Game-Configuration]PointsToWin:{self.score}")              
        except:
            self.logger.warning("[Game-Configuration]This game doesn't have points")

        try:
            self.rounds = configuration['roundsTarget']
            self.logger.info(f"[Game-Configuration]RoundsTarget:{self.rounds}")
        except:
            self.logger.warning("[Game-Configuration]This game doesn't have rounds")
           
        try:
            self.teamName = configuration['teamName']
            self.logger.info(f"[Game-Configuration]Teamname:{self.teamName}")
            self.timeStarted = configuration['gameStartedTimestamp']
        except:
            self.logger.warning("[Game-Configuration]This game doesn't have teamName/gameStartedTimestamp")

        try:
            self.timeGame = configuration['time']       
            self.logger.info(f"[Game-Configuration]Gametime:{self.timeGame}")
        except:
            self.logger.warning("[Game-Configuration]This game doesn't have time")

        try:
            self.difficulty = configuration['difficulty']  
        except:
            self.logger.warning("[Game-Configuration]This game doesn't have difficulty")

        
    def startTimers(self):

        self.gameTimer = Timer(self.timeGame, self.timeEnds)
        self.gameTimer.start()

        countDowntime = self.timeGame - 10
        self.countdownTimer = Timer(countDowntime,self.countSound)
        self.countdownTimer.start()

        self.startTime = myTimestamp()

        self.logger.info("[Gameplay-Timer]gameTimer started")
        self.logger.info("[Gameplay-Timer]countdownTimer started")    
     
        if self.final==True:
            self.resetFinal()
            if self.finalRole=="start":
                self.finalTimer = Timer(2,self.finalConstruction)
                self.finalTimer.start() 
                
    def resetTimers(self):
        try:
            if self.gameTimer.is_alive():
                self.gameTimer.cancel()
                if self.DEBUG_TIMERS: print("GameTimer stopped")
        except:
            if self.DEBUG_TIMERS: print("GameTimer is not defined")
        try:
            if self.countdownTimer.is_alive(): 
                self.countdownTimer.cancel()
                if self.DEBUG_TIMERS: print("CountdownTimer stopped")
        except:
            if self.DEBUG_TIMERS: print("CountdownTimer is not defined")
        try:
            if self.finalTimer.is_alive():
                self.finalTimer.cancel()
                if self.DEBUG_TIMERS: print("finalTimer stopped")
        except:
            if self.DEBUG_TIMERS: print("finalTimer is not defined")
        try:
            if self.buttonsTimer.is_alive():
                self.buttonsTimer.cancel()
                if self.DEBUG_TIMERS: print("buttonsTimer stopped")
        except:
           if self.DEBUG_TIMERS: print("buttonsTimer is not defined")

    def timeEnds(self):
        self.logger.info("[Room]==============TIMEOUT==============")  
        self.gameEnded(EVENTS.LOSE)

    def finalConstruction(self):
        self.wristbandNumber=0
        if "1" in self.wristbands:
            self.sendSerial("openRed")
            self.wristbandNumber+=1
        if "2" in self.wristbands:
            self.sendSerial("openPurple")
            self.wristbandNumber+=1
        if "3" in self.wristbands:
            self.sendSerial("openGreen")
            self.wristbandNumber+=1
        if "4" in self.wristbands:
            self.sendSerial("openYellow")
            self.wristbandNumber+=1
        if "5" in self.wristbands:
            self.sendSerial("openBlue")
            self.wristbandNumber+=1
        if "6" in self.wristbands:
            self.sendSerial("openOrange")
            self.wristbandNumber+=1
        self.sendSerial("checkFinal")
        self.finalStarted=True

    def enableFinal(self): 
        self.sendSerial("checkFinal") ##gia otan bei sto bubble na boroun na skanaroun 

    def resetFinal(self):
        self.finalStarted=False
        self.sendSerial("closeFinal")
        self.sendSerial("resetFinal")
        print("""=================Final Construction Reset============1.Close Final 2. Reset Final""")

    def enableRegameCallback(self):
        self.logger.info("[Regame]Is open now.")
        self.enableRegame = True

    def lockRegame(self):
        secsToWait = 5.25 #Thomas loading screen after Win
        self.enableRegame = False
        try:
            self.enableRegameTimer = Timer(secsToWait,self.enableRegameCallback)
            self.enableRegameTimer.start()
        except Exception as e:
            pass



