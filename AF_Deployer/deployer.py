import os
import fabric
import glob
from modules.pysftp import CnOpts,Connection 
import json
from invoke.watchers import StreamWatcher

class OutputWatcher(StreamWatcher):
    def submit(self, stream):
        print(f'Output: "{stream}"')
        return []

global host,room

SOFTWARE   = 'Software'
PROGRAMMER = 'Programmer'
ANYDESK    = 'Anydesk'

'''
host = "192.168.1.29"
username = "vasil"
password = "vas1998$"
port = 22
'''
host = "192.168.178.1"
username = "Mindtrap"
password = "123"
port = 22

def getCurrentPath():
    return os.path.dirname(os.path.abspath(__file__))

def getDeployFolders(rootdir):
    print(rootdir)
    folders = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            y = d.replace(rootdir,"").replace('\\', '')
            folders.append(y)
    return folders

def getAllFiles(folderPath):
    print(glob.glob(f"{folderPath}/*"))   

def executeTerminalCommand(cmd):
    global host
    c = fabric.Connection ( host = host, port = port, user = username, connect_kwargs={"password": password} , 
        # config=fabric.Config(
        # {
        #     'run': {
        #     'watchers': [
        #         OutputWatcher(),
        #     ],
        #     },
        # }) 
    )
    try:
        c.run(cmd)
    except Exception as e:
        print(e)

def createFolder(url):
    try:
        #c.run('cd c:/ & mkdir IE & cd IE & mkdir Software')     
        _url = url.replace(Home,"")
        paths = _url.split('/')
        cmd = 'cd c:/ '
        for x in paths:
            cmd+= f'& mkdir {x}'
            cmd+= f'& cd {x}'
        executeTerminalCommand(cmd)
    except Exception as e:
        print(e)

def deploy(folder,exludeFiles=None):
    global host,room
    cnopts = CnOpts()
    cnopts.hostkeys = None
    print(f"[Deployer] Folder:{folder} Room:{room} Host:{host}")
    try:
        with Connection(host, username=username, password = password , cnopts=cnopts) as sftp:
            try:
                #srcFolder = '''C:/Users/PROGregory/Documents/GitHub/AF_Controller/AF_Main_Controller''' #f'{Cur}/Mirror/{folder}'
                #destFolder = f'{Home}IE/{"AF_Main_Controller"}'
                #folder = Folders[0]
                srcFolder = f'{Cur}/Mirror/{folder}'
                destFolder = f'{Home}IE/{folder}'
                sftp.put_r(srcFolder,destFolder,excludeFiles=['config.ini'])
            except Exception as IOError:
                if IOError.args[0] == 2: #No such File
                    createFolder(destFolder)
                    sftp.put_r(srcFolder,destFolder,excludeFiles=['config.ini'])
        print(f"[Deploy] Succeed")
    except Exception as e:
        print(f"[Deploy] General Error:{e}")

def restartHost(): 
    cmd = 'shutdown /r /t 0'
    executeTerminalCommand(cmd)

def shutdownHost():
    cmd = 'shutdown /s /t 0'
    executeTerminalCommand(cmd)

def runConfig():
    cmd = 'cd c:/IE/Software & python config.py'
    executeTerminalCommand(cmd)

def sayHello():
    global room
    cmd = 'echo Hi'
    executeTerminalCommand(cmd)
    print(f"[sayHello] Room:{room}")

def anydeskRenewer():
    cmd = 'cd c:/IE/Software/anydesk && renewAnydesk.bat'
    executeTerminalCommand(cmd)

def getAnydesk():
    cmd = 'cd c:/IE/Software/anydesk && getAnydesk.bat'
    executeTerminalCommand(cmd)

def deleteFirstTimeBooted():
    cmd = 'del "c:\\Users\\Mindtrap\\.last_boot_date"'
    executeTerminalCommand(cmd)

def deleteLogs():
    cmd = 'cd c:/IE/Software/logs & del /f /q /S "*"'
    executeTerminalCommand(cmd)

def stopSoftware():
    cmd = "taskkill /IM python.exe /F & taskkill /F /IM chrome.exe /T > nul & del /S c:/IE/Software/logs/"
    executeTerminalCommand(cmd)

def startSoftware(): #Not working
    cmd = '''start "" "C:/Windows/system32/cmd.exe" "C:/Users/Mindtrap/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/startup.bat" '''
    executeTerminalCommand(cmd)

def clearLogs():
    stopSoftware()
    deleteLogs()
    #startSoftware()

def clearTrashFromProgrammer():
    cmd = 'rmdir /s /q "C:/IE/Programmer/Libraries"'
    executeTerminalCommand(cmd)


FolderToGrab = 'Mirror'
Home = '../../' #Going to C:/ in Windows
Cur = getCurrentPath()
Folders = getDeployFolders(f"{Cur}/{FolderToGrab}")

#Files = getAllFiles(f"{Cur}/{FolderToGrab}")

f = open(f'{Cur}/hostnames.json')
Hostnames = json.load(f)

canCheatRooms   = ['rabbithole','climbing','justdoit','pharaoh','thejungler','thefactory', 'bubblebobble' ] 
roomsWithLidars = ['climbing' , 'justdoit', 'pharaoh', 'pyramids', 'rabbithole', 'thejungler', 'thefactory']
roomsWithPoints = ['alleyoops','highlightbars','goal','spacejam','funinthebarn','thegulf','thepitcher','thegulf']

# [updated] climbing perimenw 
# [lidarsCalibration-Everyday]  extraFarming only for Marvin with 15 secs , 25 secs only Hardcalibration

def massJoblist():
    global host,room
    for x in Hostnames:
        room = x
        ip = Hostnames[x]
        host = ip
        try:
            if room == 'climbing':             
                sayHello()
                #getAnydesk()
                #anydeskRenewer()
                #deploy(SOFTWARE)
                #deleteFirstTimeBooted()
                #clearTrashFromProgrammer()
                #runConfig()   
                #clearLogs()
                #restartHost()
        except Exception as e:
            print(f"[massJoblist] Error:{e} IP:{host} Room:{room}")

massJoblist()