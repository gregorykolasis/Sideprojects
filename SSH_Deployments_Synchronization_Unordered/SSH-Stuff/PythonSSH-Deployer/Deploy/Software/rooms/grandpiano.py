import random
import re
from threading import Timer
import asyncio
from Libs.enums import EVENTS

'''
    checkGameCustom
    resetGameCustom()
    startGameCustom()
    standbyGameCustom()
    checkGameCustom()
'''  

class myGamecontrol:

    def __init__(self, loop=None):
        self.loop = loop
        self.maxSubrounds = 3

    def startGameCustom(self):
        self.checkNotes = False     
        self.roundCounter = 0
        self.subRound = 0

    def resetGameCustom(self):
        print('[Reset]Customgame')

    def standbyGameCustom(self):
        self.logger.info('[Standby]Grandpiano')
        self.sendSerial("closeallbuttonsleds")

    def loseScenario(self):
        self.gameEnded(EVENTS.LOSE)

    def winScenario(self):
        self.gameEnded(EVENTS.WIN)
        
    def checkGameCustom(self,msg):
        if "button" and "pressed" in msg:        
            if self.checkNotes==True:
                number = re.sub('[^0-9]', '', msg); number = int(number)  
                self.logger.info(f"[Grandpiano]Button {number} is pressed")
                self.playnotesound(str(number))            
                if number == self.buttonledopen[self.buttonCounter]:
                    self.logger.info("[Grandpiano]Correct button")
                    self.buttonCounter+=1
                    self.logger.info(f"[Grandpiano]Next should be:{self.buttonledopen[self.buttonCounter]}")
                    if self.buttonCounter >= len(self.buttonledopen):
                        self.subRound+=1
                        if self.subRound >= self.maxSubrounds:
                            self.subRound=0
                            self.roundCounter+=1
                            self.playroundsound(self.roundCounter+1)
                        else:
                            self.logger.info(f"========[SUBROUND]:{self.subRound}/{self.maxSubrounds}========")
                        if self.roundCounter >= self.rounds:
                            self.winScenario()
                        else:
                            self.logger.info(f"========[ROUND]:{self.roundCounter}/{self.rounds}========")
                            self.nextRound()
                else:
                    self.logger.info(f"[Grandpiano]Wrong button ,should be pressed ->{self.buttonledopen[self.buttonCounter]}")           
                    self.loseScenario()
        else:
            self.logger.info(f"[Grandpiano-IGNORED]Button {number} is pressed but still PLAYING NOTE-Sounds")
                
    async def playNotes(self):
        for led in self.buttonledopen:
            self.checkNotes=False
            if self.gamePlaying:
                self.sendSerial(f"openbuttonled{led}")
                self.playnotesound(led)
                await asyncio.sleep(3)
                self.sendSerial(f"closebuttonled{led}") 
        self.checkNotes=True

    def nextRound(self):
        self.buttons = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        self.buttonledopen = []
        self.buttonCounter = 0
        self.buttonCounter = 0
        self.sendSerial("closeallbuttonsleds")    
        random.shuffle(self.buttons)
        if self.players==2:
            self.buttonledopen = self.buttons[:self.players+1]
        else:
            self.buttonledopen = self.buttons[:self.players]
        self.logger.info(f"[Grandpiano]Leds Open:{self.buttonledopen}")      
        asyncio.run_coroutine_threadsafe(self.playNotes(), self.loop)
