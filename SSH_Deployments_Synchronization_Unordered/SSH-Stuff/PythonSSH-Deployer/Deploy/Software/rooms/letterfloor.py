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

    maxSubrounds = 3
    word = 0
    wordCounter = 0
    letter = 0
    letters = {
    3: {1:{'muxed','faxed','maxed','murex','muxes','exams','faxes','frump','kemps','maxes','paxes','dumka','grump','puked','redux','dumps','faked','fumed','gamps','gramp'},2:{'joypad','project','exarchy','jaspery','exocarp','hexapod','jeopardy','praecox','apteryx','exarchs','extropy','projets','hyraxes','psyched','charpoy','coaxers','cyphers','eparchy','exactor','exports'},3:{'hexapody','jeopardy','projects','exocarps','hexapods','jeopards','hardcopy','charpoys','exactors','scyphate','copyread','decrypts','dispatch','dogfaces','oxhearts','pochards','postface','scarphed','thoraxes','chapters','hypotaxes','phagocyte','copyreads','godfather','grapeshot','podcaster','chordates','goatherds','pugmark','aruspex','makeups','markups','frameup','grumped','grampus','predusk','demarks','dumpers','sparked','dampers','redguns','upgrade','defrags','grasped','sparged','remudas','desugar','sugared'}},
    4: {1:{'auspex','makeup','markup','frumps','muskeg','praxes','dumkas','grumps','maskeg','demark','dumper','gramps','gurked','kapurs','marked','masked','parked','spumed','damper','degums','pugmark','aruspex','makeups','markups','frameup','grampus','predusk','demarks','dumpers','sparked','dampers','redgums','upgrade','defrags','grasped','sparged','remudas','desugar','sugared','supermax','pugmarks','frameups','upgrades'},2:{'hypotaxes','phagocyte','copyreads','godfather','grapeshot','podcaster','chordates','goatherds','hexapody','jeopardy','projects','exocarps','hexapods','jeopards','hardcopy','charpoys','exactors','scyphate','copyread','decrypts','dispatch','dogfaces','oxhearts','pochards','postface','scarphed','thoraxes','chapters','anyhow','awheto','beachy','beacon','bejant','benchy','betcha','betony','bezant','botany','botchy','bothan','byzant','chanty','chaton','hebona','howzat','jacent','jetway','notchy','object','octane','onbeat','onycha','tawney','techo','whaten','wheaty','wotcha','zonate'},3:{'farouche','crowbait', 'butchier', 'botchier', 'berachot', 'bayonet', 'cabezon', 'chantey', 'chayote', 'cowbane', 'jaconet', 'jawbone', 'joyance', 'tachyon', 'beliquor', 'blanquet', 'cotquean', 'maroquin', 'oblique', 'qualmier', 'quotable', 'ramequin', 'aequorin', 'antiquer', 'equation', 'micawber', 'quainter', 'quantile', 'quartile', 'requinto', 'requital', 'tranquil', 'batwomen', 'crowbait', 'mowburnt', 'rumbelow', 'tubeworm', 'wamblier', 'beclamor', 'bromance', 'cenobium', 'climbout', 'clubmate', 'combater', 'combiner', 'incumber', 'outclimb', 'umbratic', 'airwomen', 'crownlet', 'lawcourt', 'outbrawl', 'outcrawl', 'timeworn', 'wariment', 'writable', 'aconitum', 'aerobium', 'albacore', 'amelcorn', 'amuletic', 'bacterin',  'baculine', 'baculite'}},
    5: {1:{'auspex','makeup','markup','frumps','muskeg','praxes','dumkas','grumps','maskeg','demark','dumper','gramps','gurked','kapurs','marked','masked','parked','spumed','damper','degums','pugmark','aruspex','makeups','markups','frameup','grampus','predusk','demarks','dumpers','sparked','dampers','redgums','upgrade','defrags','grasped','sparged','remudas','desugar','sugared','supermax','pugmarks','frameups','upgrades'},2:{'hypotaxes','phagocyte','copyreads','godfather','grapeshot','podcaster','chordates','goatherds','hexapody','jeopardy','projects','exocarps','hexapods','jeopards','hardcopy','charpoys','exactors','scyphate','copyread','decrypts','dispatch','dogfaces','oxhearts','pochards','postface','scarphed','thoraxes','chapters','anyhow','awheto','beachy','beacon','bejant','benchy','betcha','betony','bezant','botany','botchy','bothan','byzant','chanty','chaton','hebona','howzat','jacent','jetway','notchy','object','octane','onbeat','onycha','tawney','techo','whaten','wheaty','wotcha','zonate'},3:{'farouche','crowbait', 'butchier', 'botchier', 'berachot', 'bayonet', 'cabezon', 'chantey', 'chayote', 'cowbane', 'jaconet', 'jawbone', 'joyance', 'tachyon', 'beliquor', 'blanquet', 'cotquean', 'maroquin', 'oblique', 'qualmier', 'quotable', 'ramequin', 'aequorin', 'antiquer', 'equation', 'micawber', 'quainter', 'quantile', 'quartile', 'requinto', 'requital', 'tranquil', 'batwomen', 'crowbait', 'mowburnt', 'rumbelow', 'tubeworm', 'wamblier', 'beclamor', 'bromance', 'cenobium', 'climbout', 'clubmate', 'combater', 'combiner', 'incumber', 'outclimb', 'umbratic', 'airwomen', 'crownlet', 'lawcourt', 'outbrawl', 'outcrawl', 'timeworn', 'wariment', 'writable', 'aconitum', 'aerobium', 'albacore', 'amelcorn', 'amuletic', 'bacterin',  'baculine', 'baculite'}},
    6: {1:{'Auspex', 'makeup', 'markup', 'frumps', 'muskeg', 'praxes', 'dumkas', 'grumps', 'maskeg', 'demark', 'dumper', 'gramps', 'gurked', 'kapurs', 'marked', 'masked', 'parked', 'spumed', 'damper', 'degums', 'predusk', 'demarks', 'dumpers', 'sparked', 'dampers', 'redgums', 'upgrade', 'defrags', 'grasped', 'sparged', 'remudas', 'desugar', 'sugared', 'supermax', 'pugmarks', 'frameups', 'upgrades'},2:{'farouche', 'crowbait', 'butchier', 'botchier', 'berachot', 'bayonet', 'cabezon', 'chantey', 'chayote', 'cowbane', 'jaconet', 'jawbone', 'joyance', 'tachyon', 'pugmark', 'aruspex', 'makeups', 'markups', 'frameup', 'grumped', 'grampus', 'predusk', 'demarks', 'dumpers', 'sparked', 'dampers', 'redgums', 'upgrade', 'defrags',  'grasped', 'sparged', 'remudas', 'desugar', 'sugared', 'supermax', 'pugmarks', 'frameups', 'upgrades', 'cabezon', 'jawbone', 'joyance', 'jaconet', 'cowbane', 'chantey', 'tachyon', 'chayote', 'bayonet', 'abject', 'byzant', 'object', 'howzat', 'jetway', 'bezant', 'beachy', 'botchy', 'zonate', 'anyhow', 'betcha', 'chanty', 'notchy', 'wotcha', 'beacon', 'betony', 'botany', 'tawney', 'techno', 'octane'},3:{'croquante', 'equimolar', 'clubwoman', 'clubwomen', 'inquorate', 'ortanique', 'bacterium', 'bromantic', 'calembour', 'carbonium', 'columbate', 'columbine', 'columbite', 'combinate', 'metabolic', 'railwomen', 'tirewoman', 'womanlier', 'autocrime', 'balection', 'Bicornate', 'binocular', 'binuclear', 'bromelain', 'brominate', 'cabriolet', 'climature', 'coalminer', 'cobaltine', 'colubrine', 'countabl', 'cremation', 'culminate', 'incubator', 'incurable', 'interclub', 'inumbrat', 'lubrican', 'lubricat', 'manticore', 'melanotic', 'melanuric', 'monticule', 'mountable', 'mucronate', 'multicore', 'numerical', 'tambourin', 'tubicolar', 'tularemic', 'multicarbon', 'lambrequin', 'lawrencium', 'unwritable', 'bicornuate', 'orbiculate', 'tambourine', 'unmetrical', 'tourmaline', 'ulceration'}},    
    }
    problematicLetters = [
        { 'broken':'o' , 'replace':'a' }
        # { 'broken':'a' , 'replace':'i' },
        # { 'broken':'b' , 'replace':'l' },
        # { 'broken':'c' , 'replace':'v' },
        # { 'broken':'d' , 'replace':'w' },
        # { 'broken':'e' , 'replace':'n' },
        # { 'broken':'f' , 'replace':'i' },
        # { 'broken':'g' , 'replace':'l' },
        # { 'broken':'h' , 'replace':'v' },    
        # { 'broken':'j' , 'replace':'w' },
        # { 'broken':'k' , 'replace':'n' },      
        # { 'broken':'m' , 'replace':'i' },    
        # { 'broken':'o' , 'replace':'l' },
        # { 'broken':'p' , 'replace':'v' },
        # { 'broken':'q' , 'replace':'w' },
        # { 'broken':'r' , 'replace':'n' },
        # { 'broken':'s' , 'replace':'i' },
        # { 'broken':'t' , 'replace':'v' },
        # { 'broken':'u' , 'replace':'l' },  
        # { 'broken':'x' , 'replace':'w' },
        # { 'broken':'y' , 'replace':'n' },
        # { 'broken':'z' , 'replace':'i' },
    ]

    def startGameCustom(self):
        self.roundCounter = 0
        self.subRound = 0
        if self.roundCounter>3: 
            self.logger.warning(f"[Letterfloor]RoundCounter appeared to be greater than 3 epsecially:{self.roundCounter}")
            self.roundCounter=3
        self.nextRound(False)

    def resetGameCustom(self):
        print('[Reset]Customgame')

    def standbyGameCustom(self):
        self.logger.info('[Standby]Grandpiano')
        self.sendSerial("closeallbuttonsleds")

    def loseScenario(self):
        self.word = 0
        self.wordCounter = 0
        self.letter = 0
        self.gameEnded(EVENTS.LOSE)
        msg={"word":self.word,"nextletter":self.wordCounter,"gameStatus":"LOSE"}
        self.sendSCREEN(msg)         

    def winScenario(self):  
        if self.final==True and self.finalRole=="end":
            finalTimer=Timer(1,self.finalConstruction)
            finalTimer.start() 
            self.logger.info("Final opened")
        else:
            self.gameEnded(EVENTS.WIN)
            msg={"word":self.word,"nextletter":self.wordCounter,"gameStatus":"WIN"}
            self.sendSCREEN(msg)

    def checkGameCustom(self,msg):
        if "letter" in msg:
            self.letter = re.sub('[^A-Z]', '', msg)
            self.logger.info(f"[Letterfloor]Letter {self.letter} is pressed")
            if self.letter==self.word[self.wordCounter]:
                self.logger.info("[Letterfloor]Correct letter")
                self.wordCounter+=1
                self.playsound("pressed")
                msg={
                    "word":self.word,
                    "nextletter":self.wordCounter,
                    "gameStatus":"PLAYING"
                }
                self.sendSCREEN(msg)
                if self.wordCounter>=len(self.word):
                    self.logger.info(f"[Letterfloor]Word:{self.word} is completed!")
                    self.subRound+=1
                    self.wordCounter=0
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
                        self.nextRound(False)
            else:
                self.logger.info(f"[Letterfloor]Wrong letter ,should be pressed ->{self.word[self.wordCounter]}")           
                self.loseScenario()
             
    def giveWord(self,players,roundCounter):
        listname=[]
        print(f"Give Word with Players:{players} roundCounter:{roundCounter}")
        if players==2:
            listname=self.letters[players+1][roundCounter+1]
        else:
            try:
                listname=self.letters[players][roundCounter+1]
                print(f"Listanme is:{listname}")
            except Exception as e:
                print(e)
        listname=list(listname)
        random.shuffle(listname)
        
        for x in self.problematicLetters:
            listname = [s.replace( x["broken"] , x["replace"]) for s in listname]
          
        msg={
            "word":listname[0].upper(),
            "nextletter":0,
            "gameStatus":"PLAYING"
        }
        self.sendSCREEN(msg)
        return listname[0].upper()

    def nextRound(self,playSound=True):
        if playSound:
            self.playroundsound(self.roundCounter+1)
        self.word = self.giveWord(self.players,self.roundCounter)       
        self.logger.info(f"[Letterfloor]The new Word:{self.word}")    


