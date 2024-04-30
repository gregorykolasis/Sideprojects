from fabric import Connection as connection, task
import os
import glob

print(glob.glob("/home/adam/*"))


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
    return folders

def getAllFiles(folderPath):
    print(glob.glob(f"{folderPath}/*"))   


Home = '../../'
Cur = getCurrentPath()
Folders = getDeployFolders()
print(Folders)

#getAllFiles(f"{Cur}/Deploy/{Folders[0]}")

#result = Connection( host = '78.159.98.230' , port = 8822 ,  user='root' , ).run('uname -s')
#msg = f"Ran {result.command} on {result.connection.host}, got stdout:\n{result.stdout}"
#print(msg.format(result))


# with Connection(
#     host = '188.118.27.230',
#     port = 8822,
#     user = "ag3ntf4ctory",
#     connect_kwargs={"password": "1nt3ll1tz3nt!@#"}
# ) as c:
#     with c.cd("/home"):
#         c.run("ls")

import os


def deploy():
    with connection(
    host = '192.168.1.29',
    port = 22,
    user = "vasil",
    connect_kwargs={"password": "vas1998$"}
    ) as c:
        try:
            #c.run('whoami')
            #c.run('cd c:/ & mkdir IE & cd IE & mkdir Software')    
            #c.put('C:\pySsh/hi.txt', 'c:/')
            
            c.put(f'{Cur}/Deploy/{Folders[0]}', f'{Home}IE/Software')
            #c.put('C:\pySsh/hi2.txt', '../../IE/Software/hi2.txt')
        except Exception as e:
            print(e)
        
       

deploy()



