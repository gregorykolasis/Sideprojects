import os
import fabric

host     = "192.168.178.174"
username = "Mindtrap"
password = "123"
port     = 22

def executeTerminalCommand(cmd):
    with fabric.Connection( host = host, port = port, user = username, connect_kwargs={"password": password} ) as c:
        try:
            c.run(cmd)                  
        except Exception as e:
            print(e)

def restartServer():
    try:
        cmd = 'shutdown /r /t 0'
        executeTerminalCommand(cmd)
    except Exception as e:
        print(e)

restartServer()
