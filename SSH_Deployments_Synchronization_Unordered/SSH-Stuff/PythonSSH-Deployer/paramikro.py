
import os
from fabric import Connection as connection, task
import pysftp

'''
pip install pysftp
pip install fabric
'''

def getCurrentPath():
    return os.path.dirname(os.path.abspath(__file__))

def getDeployFolders():
    rootdir = f"{getCurrentPath()}/Deploy"
    folders = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            y = d.replace(rootdir,"").replace('\\', '')
            folders.append(y)
    print(folders)
    return folders

MoveHome = '../../'
Cur = getCurrentPath()
Folders = getDeployFolders()

WINDOWSUSER = os.environ['USERNAME']
host = "192.168.1.29"
username = "vasil"
password = "vas1998$"
port = 22

def createFolder(url):
    try:
        print(url)
        _url = url.replace(MoveHome,"")
        paths = _url.split('/')
        print(paths)

        with connection( host = host, port = 22, user = "vasil", connect_kwargs={"password": "vas1998$"} ) as c:
            try:
                #c.run('cd c:/ & mkdir IE & cd IE & mkdir Software')     
                cmd = 'cd c:/ '
                for x in paths:
                    cmd+= f'& mkdir {x}'
                    cmd+= f'& cd {x}'
                c.run(cmd)
                          
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)



#import paramiko
#ssh_client = paramiko.SSHClient()
# ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh_client.connect(hostname=host,port=port,username=username,password=password)
# ftp = ssh_client.open_sftp()
# files = ftp.put(f'{Cur}/Deploy/{Folders[0]}', f'{MoveHome}IE/Software')
# ftp.close()
# ssh_client.close()



with pysftp.Connection(host, username=username, password = password) as sftp:
    try:
        folder = Folders[0]
        srcFolder = f'{Cur}/Deploy/{folder}'
        destFolder = f'{MoveHome}IE/{folder}'
        sftp.put_r(srcFolder,destFolder)
    except Exception as IOError:
        if IOError.args[0] == 2: #No such File
            createFolder(destFolder)
            sftp.put_r(srcFolder,destFolder)
