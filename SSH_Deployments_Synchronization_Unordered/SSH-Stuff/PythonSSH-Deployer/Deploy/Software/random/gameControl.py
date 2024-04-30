from io import BufferedRandom
from os import read
import random
import re
from typing import final
import paho.mqtt.client as mqtt #import the client1
import time
import serial.tools.list_ports as port_list #port finder
import serial
from serial import SerialException
from serial.tools import list_ports
import asyncio 
import json 
import pygame
from threading import Timer
from decimal import Decimal
import configparser

#===================CUSTOM IMPORT-FILES===================#
from getTime import mytime 
from rpiConfiguration import makeConfiguration
from portFinder import *
from mqttConnection import *
from logMaker import setup_logger
#===================CUSTOM IMPORT-FILES===================#

global logger
sensors=['sensor1','sensor2','sensor3','sensor4','sensor5','sensor6','sensor7','sensor8','sensor9','sensor10','sensor11','sensor12','sensor13','sensor14','sensor15','sensor16','sensor17','sensor18','sensor19','sensor20'] #alley,grand,sucker punch,goal 
gamePlaying=False
gameId=0
score=0
final=0
finalStarted=0
subRound=0
wristbandNumber=0
timeGame=0
players=0
finalTimer=0
countdownTimer=0
gameTimer=0
roundCounter=0
rounds=0
host,port,username,password,startup,booted,init,reset,doorClosed,settings,scored,end,regame,error,panic,roomName,final,finalRole,deviceType,ipAddress,deviceId=makeConfiguration()

logger=setup_logger(f"{roomName}",f"{roomName}.txt")
print("Logger:ok")
passLogger(logger)

#==================================================================================ROOOM-DEPENDENT-FUNCTIONS======================================================================#
def checkRoom(msg):
    global score,gamePlaying,waitCheckflag,difficulty
    if roomName=="alleyoops"or roomName=="spacejam" or roomName=="goal":
        if search(sensors,msg):
            score=score-1
            if score==0:
                gamePlaying=False  
                logger.info("Game Finished:WIN")
                sendMQTT("WIN")
                stopMusic()
                winSound()
                standbyMode()
            else:
                soundScored()
                logger.info(f"Score:{score}")
                sendMQTT("Scored",msg)            
    elif roomName=="justdoit" or roomName=="suckerpunch" or roomName=="laserdance": #XANEIS ME ENAN AISTHTIRA
        if search(sensors,msg) or ('lightsensor' in msg and 'off' in msg):                
            logger.info("=====Sensor was triggered=======")
            score+=1
            loseGame = True       
            if roomName=='laserdance': 
                if waitCheckflag==False:
                    loseGame=False
                    score+=-1
                    logger.info("==========------------Trigger IGNORED------------==========")           
            if loseGame and roomName == 'laserdance':
                maxFails=3
                if difficulty=="MEDIUM": maxFails=2
                if difficulty=="HARD":   maxFails=1
                if difficulty=="EASY":   maxFails=3
                logger.info(f"====Fail Attempts:{score}/{maxFails}")
                if score < maxFails:          
                    loseGame=False
                
            if loseGame:
                sendMQTT("LOSE")
                gamePlaying=False
                stopMusic()
                failSound()            
                standbyMode()
            
    elif roomName=="reflections":
        checkLaserland(msg)
    elif roomName=="bubblebobble":
        checkBubble(msg)
    elif roomName=="grandpiano":
        checkGrand(msg)
    elif roomName=="letterfloor":
        checkLetter(msg)
    elif roomName=="funinthebarn":
        checkFun(msg)
    '''
    elif roomName=="joker":
        checkJoker(msg)
    '''      

def checkSerial(msg):
    global timeGame,score,gamePlaying,gameTimer,wristbandNumber,countdownTimer,finalStarted,waitCheckflag
    if msg=="doorClosed":
        sendMQTT("doorClosed")
    elif gamePlaying:
        checkRoom(msg)
    if finalStarted and gamePlaying:  
        if msg=="redScan" or msg=="purpleScan" or msg=="greenScan" or msg=="yellowScan" or msg=="blueScan" or msg=="orangeScan":
            wristbandNumber-=1
            playsound("pressed")
            logger.info(f"WristBands to be scanned:{wristbandNumber}")
        if wristbandNumber==0:
            gamePlaying=False  
            logger.info("Game ended: Win")
            stopMusic()
            winSound()
            sendMQTT("WIN")
            if roomName=="letterfloor":
                msg={"word":word,"nextletter":wordCounter,"gameStatus":"WIN"}
                sendSCREEN(msg)            
            standbyMode()


def gameStart(configuration):
    global gamePlaying,gameId,score,timeGame,gameTimer,startTime,wristbands,final,countdownTimer,finalTimer
    if gamePlaying==False:
        gamePlaying=True
        configGame(configuration)
        logger.info("""================================....Game is starting.....================================""")
        stopMusic()
        startMusic() 
        openLights()
        startTimers()
        '''
        if roomName!="laserdance":
            sendSerial("start") #start of the game
        else:
            print("[Laserdance]Custom start...")
            startTimer=Timer(1,sendSerial,["start"])
            startTimer.start()
        '''
        sendSerial("start")
        
        if roomName=="reflections":
            startLaserland()
        if roomName=="bubblebobble":
            startBubble()
        if roomName=="grandpiano":
            startGrand()
        if roomName=="letterfloor":
            startLetter()
        if roomName=="funinthebarn":
            startFun()
        '''  
        if roomName=="joker":
            startJoker()
        '''
        if roomName=="laserdance":
            startLaserdance()            
    else:
        logger.info("Game has already started")

def timeEnds():
    global final,timeGame,roomName
    logger.info(f"Time of the game -->{timeGame} is over")
    stopMusic()
    failSound()
    sendMQTT("LOSE")
    standbyMode()
    

def standbyMode():
    global gamePlaying,gameId,score,timeGame,finalStarted,wristbandNumber,final,roomName
    logger.info("======Standby Mode=====")
    gamePlaying=False  
    sendSerial("stop")
    #sendSerial("openDoor")
    resetTimers()
    score=0
    wristbandNumber=0
    timeGame=0
    logger.info("Standby:ok")  
    if final==True:
        logger.info("Reset Final")
        resetFinal()     
    if roomName=="reflections" or roomName=="laserdance":
        resetLasers()
        if roomName=="laserdance": disableChecklaserdance()
  

def gameControl (state):
    global gamePlaying,gameId
    if state=="teamRegister":
        stopMusic()
        startMusic()
        openLights()
        doorOpen()
        checkDoor() 
    elif state=="reset":
        resetRoom()
    elif state=="panic":
        sendMQTT("PANICBUTTON")        
        resetRoom() #HTAN SE SXOLIO

#==================================================================================ROOOM-DEPENDENT-FUNCTIONS======================================================================#
def sendSCREEN(msg="Unknown"):
    #lettergame
    topicName="Unknown"
    if roomName=="letterfloor":
      topicName="lettergame"
    if roomName=="joker":
      topicName="jokergame"      
    logger.info("Screen message")
    msg= json.dumps(msg)
    logger.info(f"Message:{msg} to topic: {topicName}/screen")        
    client.publish(f"{topicName}/screen", msg, qos=2 , retain=True)

def sendMQTT(reason,msg="Unknown"):
    global gameId,startTime,timeGame,score
    if reason=="doorClosed":
        logger.info(f"GameID:{gameId}")
        msg={
                "timestamp":mytime(),
                "gameId":gameId
         }
        msg= json.dumps(msg)
        logger.info(f"Message:{msg} to topic: {doorClosed}")
        client.publish(f"{doorClosed}", msg, qos=2)
    elif reason=="WIN" or reason=="LOSE" or reason=="PANICBUTTON":
        timeSpent=(mytime()-startTime)/1000
        timeSpent=round(timeSpent,0)
        timeSpent=int(timeSpent)
        timeLeft=timeGame-timeSpent
        logger.info(f"GameID:{gameId}")   
        msg={
            "timestamp":mytime(),
            "gameId":gameId,
            "reason":reason,
            "timeAllocated":timeGame,
            "timeSpent":timeSpent,
            "timeLeft":timeLeft      
            }    
        msg= json.dumps(msg)
        logger.info(f"Message:{msg} to topic: {end}")
        client.publish(f"{end}", msg, qos=2)        
    elif reason=="Scored":
        logger.info(f"GameID:{gameId}")   
        msg = {"timestamp":mytime(),"sensorName":msg,"remainingScore":score,"gameId":gameId}  
        msg = json.dumps(msg)
        logger.info(f"Message:{msg} to topic: {scored}")        
        client.publish(f"{scored}", msg, qos=2)
    elif reason=="CustomMessage":
        msg = json.dumps(msg)
        logger.info(f"Message:{msg} to topic: {scored}")        
        client.publish(f"{scored}", msg, qos=2)        

def roomInit():
    global gamePlaying,gameId,timeGame,wristbandNumber,finalStarted,rounds
    gamePlaying=False
    finalStarted=False
    gameId=None
    wristbandNumber=0
    timeGame=0
    rounds=0
    logger.info("Room:Ok")

def doorOpen():
    sendSerial("openDoor")

def checkDoor():
    sendSerial("checkDoor")

def openLights():
    sendSerial("openLights")

def closeLights():
    sendSerial("closeLights")

def resetRoom():
    global gamePlaying,gameId,score,timeGame,finalStarted,wristbandNumber,final,players,roomName
    ##edo tha ginetai reset domatiou
    logger.info("==========Reset of the game===========")
    gamePlaying=False
    
    
    sendSerial("stop")
    sendSerial("openDoor")
    closeLights()
    stopMusic()
    resetTimers()
    
    if roomName=="laserdance":
        disableChecklaserdance()     
    if roomName=="letterfloor":
        msg={"word":" ","nextletter":0,"gameStatus":"LOSE"}
        sendSCREEN(msg)    
   
    if final==True:
        resetFinal()  
    score=0
    wristbandNumber=0
    timeGame=0
    players=0
    logger.info("Reset:ok")

def resetTimers():
    global gameTimer,countdownTimer,finalTimer,rounds,buttonsTimer
    try:
        if gameTimer.is_alive():
            gameTimer.cancel() ##kano reset ton timer
            logger.info("GameTimer stopped")
    except:
        logger.info("GameTimer is not defined")
    try:
        if countdownTimer.is_alive(): 
            countdownTimer.cancel()
            logger.info("CountdownTimer stopped")
    except:
        logger.info("CountdownTimer is not defined")
    try:
        if finalTimer.is_alive():
            finalTimer.cancel()
            logger.info("finalTimer stopped")
    except:
        logger.info("finalTimer is not defined")
    try:
        if buttonsTimer.is_alive():
            buttonsTimer.cancel()
            logger.info("buttonsTimer stopped")
    except:
        logger.info("buttonsTimer is not defined")         

def configGame(configuration):
    global wristbands,score,timeGame,final,rounds,players,teamName,timeStarted,difficulty
    configuration=json.loads(configuration)
    wristbands=[configuration['playersWristbandsList'][wrist]['wristbandColor'] for wrist,x in enumerate (configuration['playersWristbandsList'])]
    players=len(wristbands)
    wristbands=(','.join(map(str,wristbands)))
    print(f"Wristbands: {wristbands}")
    logger.info(f"Wristbands: {wristbands}")
    try:
        score=configuration['pointsToWin']
        logger.info(f"Points of the game:{score}")
    except:
        logger.info("This game doesn't have points")
    try:
        rounds=configuration['roundsTarget']
        logger.info(f"Rounds of the game:{rounds}")
    except:
        logger.info("This game doesn't have rounds")  
    timeGame=configuration['time']   
    try:
        teamName=configuration['teamName']
        timeStarted=configuration['gameStartedTimestamp']
    except:
        logger.info("This game doesn't teamName/gameStartedTimestamp")  
    try:
        difficulty = configuration['difficulty']  
        logger.info(f"This game difficulty is {difficulty}")  
    except:
        logger.warning(f"Can't grab difficulty")  
    logger.info(f"Time of the game:{timeGame}")    
    logger.info(f"Final Construction: {final}")   
    
    logger.info("=========Configuration completed=========")

def startTimers():
    global gameTimer,countdownTimer,startTime
    gameTimer = Timer(timeGame, timeEnds)
    gameTimer.start()   ##ksekinaei o timer,prepei na krataei kai ton xrono pou perase
    logger.info("gameTimer started")
    countdownTimer=Timer(timeGame-10,countSound)
    countdownTimer.start()
    logger.info("countdownTimer started")    
    startTime=mytime()
    if final==True:
        resetFinal()
        logger.info("=======Final Reset========")
        if finalRole=="start":
            finalTimer=Timer(2,finalConstruction)
            finalTimer.start() 
            logger.info("finalTimer started")
    logger.info("""===================Timers started=============""")

#####GAME CONTROL#####
def makeId(msg):
    global gameId
    msg=json.loads(msg)
    gameId=msg['gameId']
    logger.info(f"GameId:{gameId}")

def finalConstruction():
    global wristbands
    global wristbandNumber
    global finalStarted
    wristbandNumber=0
   # sendSerial("openFinal")
    if "1" in wristbands:
        sendSerial("openRed")
        wristbandNumber+=1
    if "2" in wristbands:
        sendSerial("openPurple")
        wristbandNumber+=1
    if "3" in wristbands:
        sendSerial("openGreen")
        wristbandNumber+=1
    if "4" in wristbands:
        sendSerial("openYellow")
        wristbandNumber+=1
    if "5" in wristbands:
        sendSerial("openBlue")
        wristbandNumber+=1
    if "6" in wristbands:
        sendSerial("openOrange")
        wristbandNumber+=1
    sendSerial("checkFinal")
    finalStarted=True

def enableFinal():  ##gia otan bei sto bubble na boroun na skanaroun 
    sendSerial("checkFinal")

def resetFinal():
    global finalStarted
    finalStarted=False
    sendSerial("closeFinal")
    sendSerial("resetFinal")
    logger.info("""=================Final Construction Reset============
    1.Close Final 2. Reset Final""")

#=========================================================================FUNCTION-HELPERS===========================================================
def pygameInit():
    pygame.init()
    pygame.mixer.init()
    logger.info("pygame mixer:ok")
import os
defPath = os.path.abspath(os.path.join(__file__, "../"))

def startMusic():
    pygame.mixer.music.load(f'{defPath}/sounds/'+roomName+'/main.mp3')
    pygame.mixer.music.play(-1)
    logger.info("======Main theme is playing========")

def stopMusic():
    pygame.mixer.stop()
    pygame.mixer.music.stop()
    logger.info("======Music stopped========")

def soundScored():
    pygame.mixer.Sound(f'{defPath}/sounds/'+roomName+'/scored.mp3').play()
    logger.info("=======Scored sound is playing==========")
       
def failSound():
    pygame.mixer.Sound(f'{defPath}/sounds/'+roomName+'/fail.mp3').play()
    logger.info("==========faiSound is playing=============")

def winSound():
    pygame.mixer.music.load(f'{defPath}/sounds/'+roomName+'/goodjob.mp3')
    pygame.mixer.music.play()
    logger.info("=========winSound is playing=============")

def countSound():
    pygame.mixer.Sound(f'{defPath}/sounds/'+roomName+'/countdown.mp3').play()
   # pygame.mixer.music.play()
    logger.info("===========Countdown is playing=============")

def playroundsound(roundCounter):
    pygame.mixer.Sound(f'{defPath}/sounds/'+roomName+'/round'+str(roundCounter)+'.mp3').play()
   # pygame.mixer.music.play()
    logger.info(f"===========Round {roundCounter} is playing=============")
def playnotesound(button):
    pygame.mixer.Sound(f'{defPath}/sounds/'+roomName+'/button'+str(button)+'.mp3').play()
   # pygame.mixer.music.play()
    logger.info(f"===========Button: {button} is playing=============")   

def playsound(sound):
    pygame.mixer.Sound(f'{defPath}/sounds/'+roomName+'/'+sound+'.mp3').play()
   # pygame.mixer.music.play()
    logger.info(f"===========Sound {sound} is playing=============")      

def playpanic():
    pygame.mixer.Sound(f'{defPath}/sounds/panic.mp3').play()
   # pygame.mixer.music.play()
    logger.info(f"===========Sound for Panic is playing=============")       
    
def clientTranfer(mqtt):
    global client
    client=mqtt
def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

def seeVariables():
    global gamePlaying,gameId,score,timeGame,final,finalStarted,finalTimer,countdownTimer,gameTimer,wristbandNumber,players,rounds,roundCounter,subRound
    return gamePlaying,gameId,score,timeGame,final,finalStarted,finalTimer,countdownTimer,gameTimer,wristbandNumber,players,rounds,roundCounter,subRound
#=========================================================================FUNCTION-HELPERS===========================================================

###==============================================================================GRAND PIANO==============================================================================###########
def startGrand():
    global players,rounds,buttonledopen,pressedbuttons,roundCounter,subRound,buttonCounter,buttons,checkNotes
    print("start Grand")
    subRound=0
    buttons=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    buttonledopen=[]
    pressedbuttons=[]
    roundCounter=0
    checkNotes=False
    controlGrand()

  
def checkGrand(msg):
    global pressedbuttons,rounds,roundCounter,buttonCounter,subRound,buttons,buttonledopen,checkNotes
    if "button" and "pressed" in msg and checkNotes==True:
        number = re.sub('[^0-9]', '', msg)
        number=int(number)
        print(f"button {number} is pressed")
        playnotesound(str(number))
        
        print(f"Correct sounds to be pressed->{buttonledopen}")
        
        if number==buttonledopen[buttonCounter]:
            print("Correct button")
            buttonCounter+=1
            print(f"buttonCounter: {buttonCounter}")
            #if players==2 and players==buttonCounter+1 or players!=2 and players==buttonCounter:
            if buttonCounter==len(buttonledopen):
                subRound+=1
                if subRound==3:
                    subRound=0
                    roundCounter+=1
                    print("======NEXT ROUND======")    
                    playroundsound(roundCounter+1)
                print(f"====SUBROUND {subRound+1}======")
                if roundCounter==rounds:
                    logger.info("Game Finished:WIN")
                    sendMQTT("WIN")
                    gamePlaying=False
                    stopMusic()
                    winSound()
                    standbyMode()
                    sendSerial("closeallbuttonsleds")
                else:
                    controlGrand()
        else:
            stopMusic()
            failSound()
            sendMQTT("LOSE")
            standbyMode()

def grandNotes():
    global players,rounds,buttonledopen,pressedbuttons,roundCounter,gamePlaying,checkNotes
    for openled in buttonledopen:
        checkNotes=False
        if gamePlaying:
            sendSerial("openbuttonled"+str(openled))
            playnotesound(openled)
            time.sleep(3)
            sendSerial("closebuttonled"+str(openled)) 
    checkNotes=True

def controlGrand():
    global players,rounds,buttonledopen,pressedbuttons,roundCounter,subRound,buttonCounter,buttons,buttonsTimer
    buttonCounter=0
    sendSerial("closeallbuttonsleds")    
    random.shuffle(buttons)
    if players==2:
        buttonledopen=buttons[:players+1]
    else:
        buttonledopen=buttons[:players]

    print(f"==============Leds open: {buttonledopen}=================")
    buttonsTimer = Timer(4, grandNotes)
    buttonsTimer.start()
###==============================================================================GRAND PIANO==============================================================================###########

###==============================================================================BUBBLEBOBBLE==============================================================================###########
def startBubble():
    global players,rounds,buttonledopen,pressedbuttons,roundCounter,subRound
    buttons=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    buttonledopen=[]
    pressedbuttons=[]
    roundCounter=0
    subRound=0
    sendSerial("closeallbuttonsleds")
    random.shuffle(buttons)
    if players==2 or players==3:
        buttonledopen=buttons[:4]
    elif players==4:
        buttonledopen=buttons[:5]
    elif players==5:
        buttonledopen=buttons[:6]
    elif players==6:
        buttonledopen=buttons[:7]
    print(f"==============Leds open: {buttonledopen}=================")
    playroundsound(roundCounter+1)
    for openled in buttonledopen:
        sendSerial("openbuttonled"+str(openled))

def checkBubble(msg):
    global pressedbuttons,rounds,roundCounter,subRound,gamePlaying
    if "button" and "pressed" in msg:
        number = re.sub('[^0-9]', '', msg)
        number=int(number)
        print(f"button {number} is pressed")
        playsound("pressed")
        if number in buttonledopen:
            if number not in pressedbuttons: 
                print("====NEW BUTTON====")
                sendSerial("closebuttonled"+str(number))
                pressedbuttons.append(number)
                print(f"====THE PRESSED BUTTONS ARE: {pressedbuttons}=====")
            else:
                print("===BUTTON IS ALREADY OFF===")
            if len(pressedbuttons)==len(buttonledopen):
                subRound+=1
                if subRound==3:
                    subRound=0
                    print("======NEXT ROUND======")
                    roundCounter+=1
                    if roundCounter==rounds:   #---------------EDO---------------
                        if final==True and finalRole=="end":
                            finalTimer=Timer(0.01,finalConstruction)
                            finalTimer.start() 
                            logger.info("finalTimer started")
                        else:
                            logger.info("Game Finished:WIN")
                            sendMQTT("WIN")
                            gamePlaying=False
                            stopMusic()
                            winSound()
                            standbyMode()
                            sendSerial("closeallbuttonsleds")
                    else:
                        bubblenextRound()
                        print(f"================Round:{roundCounter}===============")
                        playroundsound(roundCounter+1)
                elif gamePlaying:        
                    print(f"=====SUBROUND====")
                    bubblenextRound()
        else:
            logger.info("Game Finished:LOSE")
            sendMQTT("LOSE")
            gamePlaying=False
            stopMusic()
            failSound()
            standbyMode()        
            sendSerial("closeallbuttonsleds")
        
def bubblenextRound():
    global players,rounds,buttonledopen,pressedbuttons,roundCounter,subRound   
    buttons=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    buttonledopen=[]
    pressedbuttons=[]
    sendSerial("closeallbuttonsleds")
    random.shuffle(buttons)
    if players==2 or players==3:
        buttonledopen=buttons[:4]
    elif players==4:
        buttonledopen=buttons[:5]
    elif players==5:
        buttonledopen=buttons[:6]
    elif players==6:
        buttonledopen=buttons[:7]
    print(f"==============Leds open: {buttonledopen}=================")
    for openled in buttonledopen:
        sendSerial("openbuttonled"+str(openled))      
###==============================================================================BUBBLEBOBBLE==============================================================================########### 

###==============================================================================FUNINTHEBARN==============================================================================###########
def startFun():
    global players,rounds,roundCounter,subRound,targetlights,targetCounter
    targetlights=[1,2,3,4,5,6]
    roundCounter=0
    subRound=0
    targetCounter=0
    random.shuffle(targetlights)
    sendSerial("closetargetlights") ##================= tha ginei alagi ===========================
    print(f"The random targets are: {targetlights}")
    sendSerial("opentargetlight"+str(targetlights[targetCounter]))
def nextRoundFun():
    global players,rounds,roundCounter,subRound,targetlights,targetCounter   
    targetCounter=0
    random.shuffle(targetlights)
    sendSerial("closetargetlights") ##================= tha ginei alagi ===========================
    print(f"The random targets are: {targetlights}")
    sendSerial("opentargetlight"+str(targetlights[targetCounter]))    

def checkFun(msg):
    global players,rounds,roundCounter,subRound,targetlights,targetCounter
    if "target" in msg and not "close" in msg and not "open" in msg:
        target = re.sub('[^0-9]', '', msg)
        target=int(target)
        print(f"target: {target}")
        try:
            if target==targetlights[targetCounter]:
                print("=====RIGHT TARGET=======")
                playsound("target")
                sendSerial("closetargetlight"+str(target))
                targetCounter+=1            
                if targetCounter==len(targetlights):
                    subRound+=1
                    if subRound==1:
                        subRound=0
                        roundCounter+=1
                        print(f"-------------------------------ROUNDS TO PLAY---------------------{rounds}")
                        print(f"-------------------------------ROUND COUNTER ---------------------{roundCounter}")
                        if roundCounter>=3: #roundCounter==rounds #BUG DEN STELNEI O KAPOUTSIS
                            logger.info("Game Finished:WIN")
                            sendMQTT("WIN")
                            gamePlaying=False
                            stopMusic()
                            winSound()
                            standbyMode() 
                            sendSerial("closetargetlights")                   
                        else:                    
                            print("======NEXT ROUND======")    
                            playroundsound(roundCounter+1)
                            nextRoundFun()
                    else:
                        print("=====next subround=====")
                        nextRoundFun()
                else:
                    msg="opentargetlight"+str(targetlights[targetCounter])
                    try:
                        print(msg)
                        sendSerial(msg)
                    except Exception as e:
                        print(f"GREG ERROR NOOOOOOO 1000 ->{e}")
            else:
                print("======WRONG TARGET======")
        except Exception as e:
            print(f"GREG ERROR NOOOOOOO 333333333333333333333000 ->{e}")
###==============================================================================FUNINTHEBARN==============================================================================###########
 
###==============================================================================LASERDANCE==============================================================================###########
def startLaserdance():
    global waitCheckflag
    
    waitCheckflag=False

    if waitCheckflag==False:
        timeIgnore = 3
        logger.info(f"[Laserdance]Gonna enable CHECK-SENSORS in {timeIgnore}Seconds from now...")
        enableCheck=Timer(timeIgnore,enableChecklaserdance)
        enableCheck.start()        
    
    sendSerial("openlasers")
    smokeTimer=Timer(0.5,sendSerial,["fireSmoke:7000"])
    smokeTimer.start()

def resetLasers():
    print("==================Reset lasers==================")
    sendSerial("closelasers")
    
def enableChecklaserdance():
    global waitCheckflag
    waitCheckflag=True
    logger.info(f"[Laserdance]enable waitCheckflag:{waitCheckflag}")
    
    
def disableChecklaserdance():
    global waitCheckflag
    waitCheckflag=False
    logger.info(f"[Laserdance]disable waitCheckflag:{waitCheckflag}")
    


    
###==============================================================================LASERDANCE==============================================================================###########

###==============================================================================REFLECTIONS==============================================================================###########
def startLaserland():
    global rounds,targets,lasers,lasercounter,roundCounter,players,subRound
    subRound=0
    lasercounter=0
    roundCounter=0
    targets=[1,2,3,4,5,6]
    lasers=[1,2,3,4,5,6]
    random.shuffle(targets)
    random.shuffle(lasers)
    sendSerial("closetargetlights") #Extra
    resetLasers()
    if players==2:
        targets=targets[:players+1]
        lasers=lasers[:players+1]
    else:
        targets=targets[:players]
        lasers=lasers[:players]
    print("===========LASERLAND IS STARTING============")
    print(f"The random targets are:{targets}")
    print(f"The random lasers are:{lasers}")
    sendSerial("openlaser"+str(lasers[lasercounter]))
    sendSerial("opentargetlight"+str(targets[lasercounter]))
    playroundsound(roundCounter+1)
    print("=======================================OPENING SMOKE=======================================");
    sendSerial("fireSmoke:2000");      

def checkLaserland(msg):
    global rounds,targets,lasers,subRound,lasercounter,numberposition,roundCounter,gamePlaying,players,difficulty
    try:
        if "lightsensor" in msg and "on" in msg:
            try:
                print(f"current target: {targets[lasercounter]}")
                number = re.sub('[^0-9]', '', msg)
                number=int(number)
                print(f"target {number} is on")
                if number==targets[lasercounter]:
                    lasercounter+=1
                    print("==========success,next laser============")
                    print(f"lasercounter:{lasercounter}")
                    if players>2 and lasercounter==players or players==2 and lasercounter==players+1: #htan lasercounter+1
                        subRound+=1
                        if subRound>=1:
                            subRound=0
                            print("========NEXT ROUND=======")
                            roundCounter+=1
                            print(f"----CURRENT ROUND:{roundCounter}")
                            print(f"----ROUNDS GOT FROM MQTT:{rounds}")
                                 
                            if (roundCounter>=3 and difficulty=="EASY") or (roundCounter>=5 and difficulty=="MEDIUM") or (roundCounter>=7 and difficulty=="HARD"): 
                                #HTAN roundCounter==rounds EXEI BUG den STATMATAEI sto rounds pou hrthe 
                                logger.info(f"Difficulty:{difficulty}")
                                logger.info("Game Finished:WIN")
                                sendMQTT("WIN")
                                gamePlaying=False
                                stopMusic()
                                winSound()
                                standbyMode()
                                sendSerial("closetargetlights")
                                resetLasers()                           
                            else:
                                print(f"================Round:{roundCounter+1}===============")
                                playroundsound(roundCounter+1)
                                ##shuffle ksana
                                targets=[1,2,3,4,5,6]
                                lasers=[1,2,3,4,5,6]
                                random.shuffle(targets)
                                random.shuffle(lasers)
                                if players==2:
                                    targets=targets[:players+1]
                                    lasers=lasers[:players+1]
                                else:
                                    targets=targets[:players]
                                    lasers=lasers[:players]
                                print(f"The random targets are:{targets}")
                                print(f"The random lasers are:{lasers}")
                                lasercounter=0
                                sendSerial("closetargetlights")
                                resetLasers()
                                sendSerial("openlaser"+str(lasers[lasercounter]))
                                sendSerial("opentargetlight"+str(targets[lasercounter]))
                        else:
                            print(f"================subRound:{subRound}===============")
                            ##shuffle ksana
                            targets=[1,2,3,4,5,6]
                            lasers=[1,2,3,4,5,6]
                            random.shuffle(targets)
                            random.shuffle(lasers)
                            if players==2:
                                targets=targets[:players+1]
                                lasers=lasers[:players+1]
                            else:
                                targets=targets[:players]
                                lasers=lasers[:players]
                            print(f"The random targets are:{targets}")
                            print(f"The random lasers are:{lasers}")
                            lasercounter=0
                            time.sleep(1)
                            sendSerial("closetargetlights")
                            resetLasers()
                            sendSerial("openlaser"+str(lasers[lasercounter]))
                            sendSerial("opentargetlight"+str(targets[lasercounter]))        
                    elif lasercounter<6 and gamePlaying:
                       # print("=======SUBROUND======")
                        sendSerial("openlaser"+str(lasers[lasercounter]))
                        sendSerial("opentargetlight"+str(targets[lasercounter]))
                        print(f"next target is {targets[lasercounter]} ")
                        for item in targets[lasercounter:]:
                            sendSerial("checklightsensor"+str(item))
            except Exception as e:
                print(f"[Greg-Error] if 'lightsensor' in msg and 'on' in msg:  --->{e}")             
        elif "lightsensor" in msg and "off" in msg:
            try:
                number = re.sub('[^0-9]', '', msg)
                number=int(number)
                print(f"target {number} is off")
                try:
                    numberposition = targets.index(number)
                    print(f"number position: {numberposition}")
                    if numberposition<=lasercounter:
                        if numberposition==0:
                            lasercounter=numberposition
                        else:
                            lasercounter=numberposition
                        print(f"to lasercounter einai tora{lasercounter}")
                        print("prepei na kleisoun kapoia laser kai stoxoi")
                        for item in targets[lasercounter+1:]:
                            sendSerial("closetargetlight"+str(item))
                        for item in lasers[lasercounter+1:]:
                           sendSerial("closelaser"+str(item))
                except:
                    pass
            except Exception as e:
                print(f"[Greg-Error] elif 'lightsensor' in msg and 'off' in msg:  --->{e}")                   
    except Exception as e:
        print(f"[Greg-Error] MAIN-Error--->{e}")
###==============================================================================REFLECTIONS==============================================================================###########


###==============================================================================LETTERFLOOR==============================================================================###########
def startLetter():
    global players,rounds,roundCounter,subRound,word,wordCounter
    wordCounter=0
    subRound=0
    print("=======GAME LETTER STARTED======")
    roundCounter=0
    word=giveLetter(players,roundCounter)
    print(f"THE WORD IS: {word}")
    print(f"letter:{word[wordCounter]}")
def giveLetter(players,roundCounter):
#    global players,roundCounter
    print("give letter")
    listname=[]
    letters={
    3: {1:{'muxed','faxed','maxed','murex','muxes','exams','faxes','frump','kemps','maxes','paxes','dumka','grump','puked','redux','dumps','faked','fumed','gamps','gramp'},2:{'joypad','project','exarchy','jaspery','exocarp','hexapod','jeopardy','praecox','apteryx','exarchs','extropy','projets','hyraxes','psyched','charpoy','coaxers','cyphers','eparchy','exactor','exports'},3:{'hexapody','jeopardy','projects','exocarps','hexapods','jeopards','hardcopy','charpoys','exactors','scyphate','copyread','decrypts','dispatch','dogfaces','oxhearts','pochards','postface','scarphed','thoraxes','chapters','hypotaxes','phagocyte','copyreads','godfather','grapeshot','podcaster','chordates','goatherds','pugmark','aruspex','makeups','markups','frameup','grumped','grampus','predusk','demarks','dumpers','sparked','dampers','redguns','upgrade','defrags','grasped','sparged','remudas','desugar','sugared'}},
    4: {1:{'auspex','makeup','markup','frumps','muskeg','praxes','dumkas','grumps','maskeg','demark','dumper','gramps','gurked','kapurs','marked','masked','parked','spumed','damper','degums','pugmark','aruspex','makeups','markups','frameup','grampus','predusk','demarks','dumpers','sparked','dampers','redgums','upgrade','defrags','grasped','sparged','remudas','desugar','sugared','supermax','pugmarks','frameups','upgrades'},2:{'hypotaxes','phagocyte','copyreads','godfather','grapeshot','podcaster','chordates','goatherds','hexapody','jeopardy','projects','exocarps','hexapods','jeopards','hardcopy','charpoys','exactors','scyphate','copyread','decrypts','dispatch','dogfaces','oxhearts','pochards','postface','scarphed','thoraxes','chapters','anyhow','awheto','beachy','beacon','bejant','benchy','betcha','betony','bezant','botany','botchy','bothan','byzant','chanty','chaton','hebona','howzat','jacent','jetway','notchy','object','octane','onbeat','onycha','tawney','techo','whaten','wheaty','wotcha','zonate'},3:{'farouche','crowbait', 'butchier', 'botchier', 'berachot', 'bayonet', 'cabezon', 'chantey', 'chayote', 'cowbane', 'jaconet', 'jawbone', 'joyance', 'tachyon', 'beliquor', 'blanquet', 'cotquean', 'maroquin', 'oblique', 'qualmier', 'quotable', 'ramequin', 'aequorin', 'antiquer', 'equation', 'micawber', 'quainter', 'quantile', 'quartile', 'requinto', 'requital', 'tranquil', 'batwomen', 'crowbait', 'mowburnt', 'rumbelow', 'tubeworm', 'wamblier', 'beclamor', 'bromance', 'cenobium', 'climbout', 'clubmate', 'combater', 'combiner', 'incumber', 'outclimb', 'umbratic', 'airwomen', 'crownlet', 'lawcourt', 'outbrawl', 'outcrawl', 'timeworn', 'wariment', 'writable', 'aconitum', 'aerobium', 'albacore', 'amelcorn', 'amuletic', 'bacterin',  'baculine', 'baculite'}},
    5: {1:{'auspex','makeup','markup','frumps','muskeg','praxes','dumkas','grumps','maskeg','demark','dumper','gramps','gurked','kapurs','marked','masked','parked','spumed','damper','degums','pugmark','aruspex','makeups','markups','frameup','grampus','predusk','demarks','dumpers','sparked','dampers','redgums','upgrade','defrags','grasped','sparged','remudas','desugar','sugared','supermax','pugmarks','frameups','upgrades'},2:{'hypotaxes','phagocyte','copyreads','godfather','grapeshot','podcaster','chordates','goatherds','hexapody','jeopardy','projects','exocarps','hexapods','jeopards','hardcopy','charpoys','exactors','scyphate','copyread','decrypts','dispatch','dogfaces','oxhearts','pochards','postface','scarphed','thoraxes','chapters','anyhow','awheto','beachy','beacon','bejant','benchy','betcha','betony','bezant','botany','botchy','bothan','byzant','chanty','chaton','hebona','howzat','jacent','jetway','notchy','object','octane','onbeat','onycha','tawney','techo','whaten','wheaty','wotcha','zonate'},3:{'farouche','crowbait', 'butchier', 'botchier', 'berachot', 'bayonet', 'cabezon', 'chantey', 'chayote', 'cowbane', 'jaconet', 'jawbone', 'joyance', 'tachyon', 'beliquor', 'blanquet', 'cotquean', 'maroquin', 'oblique', 'qualmier', 'quotable', 'ramequin', 'aequorin', 'antiquer', 'equation', 'micawber', 'quainter', 'quantile', 'quartile', 'requinto', 'requital', 'tranquil', 'batwomen', 'crowbait', 'mowburnt', 'rumbelow', 'tubeworm', 'wamblier', 'beclamor', 'bromance', 'cenobium', 'climbout', 'clubmate', 'combater', 'combiner', 'incumber', 'outclimb', 'umbratic', 'airwomen', 'crownlet', 'lawcourt', 'outbrawl', 'outcrawl', 'timeworn', 'wariment', 'writable', 'aconitum', 'aerobium', 'albacore', 'amelcorn', 'amuletic', 'bacterin',  'baculine', 'baculite'}},
    6: {1:{'Auspex', 'makeup', 'markup', 'frumps', 'muskeg', 'praxes', 'dumkas', 'grumps', 'maskeg', 'demark', 'dumper', 'gramps', 'gurked', 'kapurs', 'marked', 'masked', 'parked', 'spumed', 'damper', 'degums', 'predusk', 'demarks', 'dumpers', 'sparked', 'dampers', 'redgums', 'upgrade', 'defrags', 'grasped', 'sparged', 'remudas', 'desugar', 'sugared', 'supermax', 'pugmarks', 'frameups', 'upgrades'},2:{'farouche', 'crowbait', 'butchier', 'botchier', 'berachot', 'bayonet', 'cabezon', 'chantey', 'chayote', 'cowbane', 'jaconet', 'jawbone', 'joyance', 'tachyon', 'pugmark', 'aruspex', 'makeups', 'markups', 'frameup', 'grumped', 'grampus', 'predusk', 'demarks', 'dumpers', 'sparked', 'dampers', 'redgums', 'upgrade', 'defrags',  'grasped', 'sparged', 'remudas', 'desugar', 'sugared', 'supermax', 'pugmarks', 'frameups', 'upgrades', 'cabezon', 'jawbone', 'joyance', 'jaconet', 'cowbane', 'chantey', 'tachyon', 'chayote', 'bayonet', 'abject', 'byzant', 'object', 'howzat', 'jetway', 'bezant', 'beachy', 'botchy', 'zonate', 'anyhow', 'betcha', 'chanty', 'notchy', 'wotcha', 'beacon', 'betony', 'botany', 'tawney', 'techno', 'octane'},3:{'croquante', 'equimolar', 'clubwoman', 'clubwomen', 'inquorate', 'ortanique', 'bacterium', 'bromantic', 'calembour', 'carbonium', 'columbate', 'columbine', 'columbite', 'combinate', 'metabolic', 'railwomen', 'tirewoman', 'womanlier', 'autocrime', 'balection', 'Bicornate', 'binocular', 'binuclear', 'bromelain', 'brominate', 'cabriolet', 'climature', 'coalminer', 'cobaltine', 'colubrine', 'countabl', 'cremation', 'culminate', 'incubator', 'incurable', 'interclub', 'inumbrat', 'lubrican', 'lubricat', 'manticore', 'melanotic', 'melanuric', 'monticule', 'mountable', 'mucronate', 'multicore', 'numerical', 'tambourin', 'tubicolar', 'tularemic', 'multicarbon', 'lambrequin', 'lawrencium', 'unwritable', 'bicornuate', 'orbiculate', 'tambourine', 'unmetrical', 'tourmaline', 'ulceration'}}    
    #6: {1:{'lll'},2:{'lll'},3:{'lll'},4:{'lll'},5:{'lll'},6:{'lll'}}
    }
    if players==2:
        listname=letters[players+1][roundCounter+1]
    else:
        listname=letters[players][roundCounter+1]
    listname=list(listname)
    random.shuffle(listname)
    msg={
      "word":listname[0].upper(),
      "nextletter":0,
      "gameStatus":"PLAYING"
    }
    sendSCREEN(msg)
    return listname[0].upper()
def checkLetter(msg):
    global word,wordCounter,letter,subRound,roundCounter,rounds
    if "letter" in msg:
        letter = re.sub('[^A-Z]', '', msg)
        print(f"letter {letter}")
        if letter==word[wordCounter]:
            print("Right letter pressed")
            wordCounter+=1
            playsound("pressed")
            msg={
            "word":word,
            "nextletter":wordCounter,
            "gameStatus":"PLAYING"
                }
            sendSCREEN(msg)
            if wordCounter==len(word):
                print("Word completed")
                subRound+=1
                wordCounter=0
                if subRound==3:
                    subRound=0
                    roundCounter+=1
                    if roundCounter==rounds:
                        if final==True and finalRole=="end":
                            finalTimer=Timer(1,finalConstruction)
                            finalTimer.start() 
                            logger.info("finalTimer started")
                        else:
                            logger.info("Game Finished:WIN")
                            sendMQTT("WIN")
                            gamePlaying=False
                            stopMusic()
                            winSound()
                            standbyMode()
                            msg={"word":word,"nextletter":wordCounter,"gameStatus":"WIN"}
                            sendSCREEN(msg)
                    else:
                        print("======NEXT ROUND======")    
                        playroundsound(roundCounter+1)
                        word=giveLetter(players,roundCounter)       
                        print(f"The word is {word}")   
                else:
                    print(f"====SUBROUND {subRound+1}======")
                    word=giveLetter(players,roundCounter)       
                    print(f"The word is {word}")    
            else:
                print(f"next letter {word[wordCounter]}")                          
        else:
            stopMusic()
            failSound()
            sendMQTT("LOSE")
            standbyMode()
            msg={"word":word,"nextletter":wordCounter,"gameStatus":"LOSE"}
            sendSCREEN(msg)
###==============================================================================LETTERFLOOR==============================================================================###########
