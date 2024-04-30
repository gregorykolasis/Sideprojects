import os
from uuid import uuid4
try:
    from configparser import ConfigParser, ExtendedInterpolation
except ModuleNotFoundError as e:
    os.system("pip install configparser")

global Configuration
Configuration = None

file = "config.ini"

def initConfiguration():
    global Configuration
    if Configuration is None:
        try:         
            config = evaluateConfigfile()
            obj = dict()

            obj["roomName"]    = config['ROOM']['roomName']
            uuid = f"{obj['roomName']}Gameplay_{str(uuid4())[:6]}"

            config.set('ID','deviceId',f"{uuid}")
            with open(file, 'w') as configfile:
                config.write(configfile) 
                  
            obj["host"]        = config['CONNECTION']['host']
            obj["port"]        = config['CONNECTION']['port']
            obj["username"]    = config['CONNECTION']['username']
            obj["password"]    = config['CONNECTION']['password']
            obj["deviceId"]    = config['ID']['deviceid']

            obj["startup"]     = config['TOPICS']['startup']
            obj["booted"]      = config['TOPICS']['booted']
            obj["init"]        = config['TOPICS']['init']
            obj["reset"]       = config['TOPICS']['reset']
            obj["doorClosed"]  = config['TOPICS']['doorclosed']
            obj["settings"]    = config['TOPICS']['settings']
            obj["scored"]      = config['TOPICS']['scored']
            obj["end"]         = config['TOPICS']['end']
            obj["regame"]      = config['TOPICS']['regame']
            obj["error"]       = config['TOPICS']['error']
            obj["panic"]       = config['TOPICS']['panic']
            obj["choosedifficulty"] = config['TOPICS']['choosedifficulty']
            obj["changeLanguage"]       = config['TOPICS']['changeLanguage']
           
            obj["final"]       = config['ROOM'].getboolean('final')
            obj["finalRole"]   = config['ROOM']['finalRole']
            obj["deviceType"]  = config['ROOM']['devicetype']
            

            Configuration = obj
        except Exception as e:
            print(f"[Configuration]Can't be parsed or edited Error:{e}")
    else:
        print("[Configuration]Is already completed!")        
        
def getConfiguration():  
    global Configuration
    return Configuration
    
def evaluateConfigfile():
    config = ConfigParser(strict=False,interpolation = ExtendedInterpolation())
    defPath = os.path.abspath(os.path.join(__file__, "../../"))
    pathfilename = f"{defPath}/{file}"   
    exist = os.path.exists(pathfilename)
    if not exist:
        print(f"[Configuration]This filename doens't exist:{pathfilename}\nExiting...")
        exit()
    config.read(pathfilename) 
    print(f"[Configuration]Sections:{config.sections()}")      
    return config