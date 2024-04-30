import os,random

try:
    import pygame
except ModuleNotFoundError as e:
    os.system("pip install pygame")
    
class myMusic:

    currentSound = None
    oldFileSystem = False

    def __init__(self):
        self.defPath = os.path.abspath(os.path.join(__file__, "../../assets/"))    
        self.pygameInit()
        
    def pygameInit(self):
        pygame.init()
        pygame.mixer.init()

    def mixerMusicPlay(self, file , repeat = False):
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.load(file)
        if repeat: pygame.mixer.music.play(-1)
        else: pygame.mixer.music.play()

    def mixerSoundPlay(self, file , repeat = False):
        self.currentSound = pygame.mixer.Sound(file)
        self.currentSound.play()

    def stopMusic(self):
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.logger.info("[Music]Stopped")
        
    def playDrum(self):
        mp3s = None
        if self.difficulty == 'EASY': mp3s = ['Drums']#,'Attack1','Attack2','Attack3']
        elif self.difficulty == 'MEDIUM': mp3s = ['Attack1']
        elif self.difficulty == 'HARD': mp3s = ['Attack3']
        else: mp3s = ['Drums']
        file = f'{self.defPath}/sounds/__common__/bass/{random.choice(mp3s)}.mp3'
        try:
            self.mixerSoundPlay(file)  
        except Exception as e:
            self.logger.error(f"[playDrum] Error:{e}")

    def playRegistration(self):
        file  = f'{self.defPath}/sounds/__common__/registration.mp3'      
        try:
            self.mixerMusicPlay(file , True)
            self.logger.info("[Music]Main Theme")
        except Exception as e:
            self.logger.error(f"[playRegistration] Error:{e}")

    def playMain(self):
        file  = f'{self.defPath}/sounds/{self.roomName}/main.mp3'
        try:    
            self.mixerMusicPlay(file , True)
            self.logger.info("[Music]Main")
        except Exception as e:
            self.logger.error(f"[playMain] Error:{e}")

    def startSound(self):
        file = f'{self.defPath}/sounds/__common__/start_3_2_1.mp3'
        try:
            self.mixerSoundPlay(file)  
        except Exception as e:
            self.logger.error(f"[startSound] Error:{e}")

    def countSound(self):
        file = f'{self.defPath}/sounds/__common__/countdown.mp3'
        try:
            pygame.mixer.music.set_volume(0.5)
            self.mixerSoundPlay(file)  
            self.logger.info("[Music]Countdown")
        except Exception as e:
            self.logger.error(f"[countSound] Error:{e}")

    def failSound(self):
        file = f'{self.defPath}/sounds/__common__/fail.mp3'
        try:
            self.mixerSoundPlay(file)  
            self.logger.info("[Sound]Failsound")
        except Exception as e:
            self.logger.error(f"[failSound] Error:{e}")

    def winSound(self):
        file = f'{self.defPath}/sounds/__common__/goodjob.mp3'
        try:
            self.mixerMusicPlay(file)
            self.logger.info("[Music]Winsound")
        except Exception as e:
            self.logger.error(f"[winSound] Error:{e}")

    def playroundsound(self,roundCounter):
        try:
            file = f'{self.defPath}/sounds/__common__/rounds/round{roundCounter}.mp3'
            self.mixerSoundPlay(file)  
            self.logger.info(f"[Sound]Round:{roundCounter}")
        except Exception as e:
            self.logger.error(f"[playroundsound] Error:{e}")

    def soundApplause(self):
        file = f'{self.defPath}/sounds/__common__/effects/applause.mp3'
        try:
            self.mixerSoundPlay(file)
            self.logger.info("[Music]Scored")
        except Exception as e:
            self.logger.error(f"[soundApplause] Error:{e}")
            
    def soundSplash(self):
        file = f'{self.defPath}/sounds/__common__/effects/splash.mp3'
        try:
            self.mixerSoundPlay(file)
            self.logger.info("[Music]Splash")
        except Exception as e:
            self.logger.error(f"[Splash] Error:{e}")

    def playNote(self,button):
        file = f'{self.defPath}/sounds/grandpiano/notes/button{button}.mp3'
        try:
            self.mixerSoundPlay(file)
            self.logger.info(f"[Sound]Grandpiano Note:{button}")
        except Exception as e:
            self.logger.error(f"[playNote] Error:{e}")   
            
    def playButton(self,name):
        file = f'{self.defPath}/sounds/__common__/buttons/{name}.mp3'
        try:
            self.mixerSoundPlay(file)
        except Exception as e:
            self.logger.error(f"[playButton] Error:{e}")       

    def playsound(self,sound):
        if sound == 'pressed':
            mp3s = ['Pokemon','Sonic','8Bit','Coin']
            file = f'{self.defPath}/sounds/__common__/buttons/{random.choice(mp3s)}.mp3'
        if 'airshot' in sound:
            file = f'{self.defPath}/sounds/__common__/airshots/{sound}.mp3'   
        if sound == 'laser' or sound == 'targetlost' or sound=='targetoff':
            file = f'{self.defPath}/sounds/__common__/lasers/{sound}.mp3'   
        try:
            self.mixerSoundPlay(file)
            self.logger.info(f"[Sound]{sound}")
        except Exception as e:
            self.logger.error(f"[playsound] Error:{e}") 

    def playScan(self):
        file = f'{self.defPath}/sounds/__common__/scan/Beep.mp3'
        try:
            self.mixerSoundPlay(file)
            self.logger.info(f"[playScan]")
        except Exception as e:
            self.logger.error(f"[playScan] Error:{e}")     

    def playPanic(self):
        file = f'{self.defPath}/sounds/__common__/panic/Cancel.mp3'
        try:
            self.mixerSoundPlay(file)
            self.logger.info(f"[playScan]")
        except Exception as e:
            self.logger.error(f"[playScan] Error:{e}")

    def playFail(self,name):
        file = f'{self.defPath}/sounds/__common__/fail/{name}.mp3'
        try:
            self.mixerSoundPlay(file)
        except Exception as e:
            self.logger.error(f"[playButton] Error:{e}") 