import os
import fabric
import glob
from modules.pysftp import CnOpts,Connection 
import json

global host
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
    with fabric.Connection( host = host, port = port, user = username, connect_kwargs={"password": password} ) as c:
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

def deploy():
    global host
    cnopts = CnOpts()
    cnopts.hostkeys = None
    print(f"[deploy]Host:{host}")
    with Connection(host, username=username, password = password , cnopts=cnopts) as sftp:
        try:
            #srcFolder = '''C:/Users/PROGregory/Documents/GitHub/AF_Controller/AF_Main_Controller''' #f'{Cur}/Mirror/{folder}'
            #destFolder = f'{Home}IE/{"AF_Main_Controller"}'
            folder = Folders[0]
            srcFolder = f'{Cur}/Mirror/{folder}'
            destFolder = f'{Home}IE/{folder}'
            sftp.put_r(srcFolder,destFolder,excludeFiles=['config.ini'])
        except Exception as IOError:
            if IOError.args[0] == 2: #No such File
                createFolder(destFolder)
                sftp.put_r(srcFolder,destFolder,excludeFiles=['config.ini'])

def restartHost():
    cmd = 'shutdown /r /t 0'
    executeTerminalCommand(cmd)

FolderToGrab = 'Mirror'
Home = '../../' #Going to C:/ in Windows
Cur = getCurrentPath()
Folders = getDeployFolders(f"{Cur}/{FolderToGrab}")
Files = getAllFiles(f"{Cur}/{FolderToGrab}")

f = open(f'{Cur}/hostnames.json')
Hostnames = json.load(f)

def deployMirror():
    global host
    for x in Hostnames:
        room = x
        ip = Hostnames[x]
        if room=='justdoit':
            print(f"[Mirorring]For:{room} at IP:{ip}")
            host = ip
            try:
                deploy()
                restartHost()
            except Exception as e:
                print(f"[deploy] Error:{e}")

deployMirror()