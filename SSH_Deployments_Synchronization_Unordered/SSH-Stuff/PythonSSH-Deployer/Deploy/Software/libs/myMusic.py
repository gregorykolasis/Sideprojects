import os

try:
    import pygame
except ModuleNotFoundError as e:
    os.system("pip install pygame")
    
class myMusic:
    def __init__(self):
        self.defPath = os.path.abspath(os.path.join(__file__, "../../assets/"))    
        #self.logger.info(f"[Music]defPath:{self.defPath}")
        self.pygameInit()
        
    def pygameInit(self):
        pygame.init()
        pygame.mixer.init()
        #self.logger.info("[Music]Mixer ready")

    def startMusic(self):
        pygame.mixer.music.load(f'{self.defPath}/sounds/'+self.roomName+'/main.mp3')
        pygame.mixer.music.play(-1)
        self.logger.info("[Music]Main Theme")

    def stopMusic(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.logger.info("[Music]Stopped")

    def soundScored(self):
        pygame.mixer.Sound(f'{self.defPath}/sounds/'+self.roomName+'/scored.mp3').play()
        self.logger.info("[Music]Scored")
           
    def failSound(self):
        pygame.mixer.Sound(f'{self.defPath}/sounds/'+self.roomName+'/fail.mp3').play()
        self.logger.info("[Music]Failsound")

    def winSound(self):
        pygame.mixer.music.load(f'{self.defPath}/sounds/'+self.roomName+'/goodjob.mp3')
        pygame.mixer.music.play()
        self.logger.info("[Music]Winsound")

    def countSound(self):
        pygame.mixer.Sound(f'{self.defPath}/sounds/'+self.roomName+'/countdown.mp3').play()
        #pygame.mixer.music.play()
        self.logger.info("[Music]Countdown")

    def playroundsound(self,roundCounter):
        pygame.mixer.Sound(f'{self.defPath}/sounds/'+self.roomName+'/round'+str(roundCounter)+'.mp3').play()
        #pygame.mixer.music.play()
        self.logger.info(f"[Music]Round:{roundCounter}")
    def playnotesound(self,button):
        pygame.mixer.Sound(f'{self.defPath}/sounds/'+self.roomName+'/button'+str(button)+'.mp3').play()
        #pygame.mixer.music.play()
        self.logger.info(f"[Music]Button:{button}")   

    def playsound(self,sound):
        pygame.mixer.Sound(f'{self.defPath}/sounds/'+self.roomName+'/'+sound+'.mp3').play()
        #pygame.mixer.music.play()
        self.logger.info(f"[Music]Sound:{sound}")      

    def playpanic(self):
        pygame.mixer.Sound(f'{self.defPath}/sounds/panic.mp3').play()
        #pygame.mixer.music.play()
        self.logger.info(f"[Music]Panic")