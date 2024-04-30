import random
import re
from threading import Timer
from Libs.enums import EVENTS

'''
    checkGameCustom
    resetGameCustom()
    startGameCustom()
    standbyGameCustom()
'''    

class myGamecontrol:

    def __init__(self, loop=None):
        self.loop = loop

    maxSubrounds = 3

    def resetGameCustom(self):
        self.resetScenario()

    def standbyGameCustom(self):
        self.resetScenario()
        
    def nextRound(self):
        self.buttons = [1,2,3,4,5,6]#[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
        self.buttonledopen = []
        self.pressedbuttons = []
        self.sendSerial("closeallbuttonsleds")
        random.shuffle(self.buttons)
        if self.players == 2 or self.players == 3:
            self.buttonledopen = self.buttons[:4]
        elif self.players == 4:
            self.buttonledopen = self.buttons[:5]
        elif self.players == 5:
            self.buttonledopen = self.buttons[:6]
        elif self.players == 6:
            self.buttonledopen = self.buttons[:7]
        self.logger.info(f"[Bubblebobble]Leds Open:{self.buttonledopen}")
        for led in self.buttonledopen:
            self.sendSerial(f"openbuttonled{led}")

    def winScenario(self):
        if self.final==True and self.finalRole=="end":
            finalTimer=Timer(1, self.finalConstruction)
            finalTimer.start() 
            self.logger.info("[Final]Opened")
        else:
            self.gameEnded(EVENTS.WIN)
            self.resetScenario()
    
    def loseScenario(self):
        self.gameEnded(EVENTS.LOSE)
        self.resetScenario()

    def resetScenario(self):
        self.sendSerial("closeallbuttonsleds")

    def startGameCustom(self):   
        self.roundCounter=0
        self.subRound=0
        self.nextRound()

    def checkGameCustom(self,msg):
        if "button" and "pressed" in msg:
            number = re.sub('[^0-9]', '', msg)
            number = int(number)
            if number in self.buttonledopen:
                if number not in self.pressedbuttons: 
                    self.playsound("pressed")
                    self.logger.info(f"[Bubblebobble]Correct Button {number} is pressed")
                    self.sendSerial(f"closebuttonled{number}")
                    self.pressedbuttons.append(number)
                    self.logger.info(f"[Bubblebobble]Pressed buttons:{self.pressedbuttons}")
                else:
                    self.logger.info(f"[Bubblebobble]This Button {number} is already pressed")
                if len(self.pressedbuttons)>=len(self.buttonledopen):
                    self.subRound+=1
                    if self.subRound>=self.maxSubrounds:
                        self.subRound=0       
                        self.roundCounter+=1
                        if self.roundCounter>=self.rounds:
                            self.roundCounter=0
                            self.winScenario()
                        else:
                            self.logger.info(f"========[ROUND]:{self.roundCounter}/{self.rounds}========")
                            self.playroundsound(self.roundCounter+1)
                            self.nextRound()
                    else:        
                        self.logger.info(f"========[SUBROUND]:{self.subRound}/{self.maxSubrounds}========")
                        self.nextRound()
            else:
                self.loseScenario()