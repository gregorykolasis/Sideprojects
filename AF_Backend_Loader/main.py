import datetime
import os
import subprocess
import threading
import logging
import time
import signal
import sys

path = os.path.abspath(os.path.join(__file__, "../"))

from libs.myLogger import setLogger
from libs.utils import restartScript,getPlatform

JAR_FILE_NAME = 'services-0.0.1-SNAPSHOT.jar'

import optparse
def parser(unparsed_args):
  
  parser = optparse.OptionParser(
    usage = "%prog [options]",
    description = "Run jar file directly from python and capture standard output/error and log them to files with datetimes as filenames"
  )
  # destination ip and port
  group = optparse.OptionGroup(parser, "Prerun")
  group.add_option("-a", "--delay",
    dest = "delay",
    action = "store",
    help = "Value in seconds to be waited before the script will run",
    default = 0
  )
  parser.add_option_group(group)

  # auth
  group = optparse.OptionGroup(parser, "Afterrun")
  group.add_option("-b", "--no-restart",
    dest = "restart",
    help = "If 'Timed out as no activity' is printed it will force restart Java.",
    action = "store_false",
    default = True
  )
  parser.add_option_group(group)

  (options, args) = parser.parse_args(unparsed_args)

  return options

class myMain():

    def __init__(self):
        self.main()
              
    SESSION_LOGGING = True
    PRODUCTION = True
    roomName = 'agentfactory_services'
    runningProcess = None

    def setupLogger(self,loggingType):
        if self.SESSION_LOGGING:
            now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
            date = datetime.datetime.now().strftime('%Y_%m_%d')
            subFolder = f"{self.roomName}_Session_{date}"
            subFolderPath = f"{path}/logs/{subFolder}"
            isExist = os.path.exists(subFolderPath)
            if not isExist:
                os.makedirs(subFolderPath)
            filename = f"{subFolderPath}/{self.roomName}_{now}.log" 
        else:
            filename = f"{path}/logs/{self.roomName}.log"    
        setLogger(filename,loggingType)
        self.logger = logging.getLogger()

    def read_output(self, pipe, role):
        for line in iter(pipe.readline, ''):
            data = line.rstrip('\n')
            dataType = 'INFO'
            if role == 'STDERR' or 'ERROR' in data:
                dataType = 'ERROR'
                self.logger.error(data)
            elif 'WARN' in data:
                dataType = 'WARNING'
                self.logger.warning(data)
            elif 'DEBUG' in data:
                dataType = 'DEBUG'
                self.logger.debug(data)
            elif role == 'STDOUT':
                dataType = 'INFO'
                self.logger.info(data)
            else:
                dataType = 'UNKNOWN'
                self.logger.critical(data)  
            if dataType=='ERROR':
                if 'Timed out as no activity' in data:
                    self.logger.critical("[-----------------SELF--------------] Gonna restart backend lost the MQTT Connection again...!")
                    self.restart()
            # if 'Pinging...' in data:
            #     self.restart()

    def restart(self):
        self.stopSubprocess()
        restartScript()

    def stopSubprocess(self):
        if getPlatform()=='windows':
            try:
                subprocess.run(['taskkill', '/F', '/IM', 'java.exe'], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception as e:
                pass
        else:
            try:
                if self.runningProcess:
                    os.killpg(os.getpgid(self.runningProcess.pid), signal.SIGKILL)
            except Exception as e:
                self.logger.critical(f"[-----------------SELF--------------] Can't kill process Error:{e}")
            try:
                os.system("killall -9 java")
            except:
                pass


    def runSubproccess(self,command):
        if getPlatform()=='windows': 
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1 , shell=True )
        else:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1 , shell=True , preexec_fn=os.setsid )
        self.runningProcess = process
        stdout_thread = threading.Thread( target = self.read_output, args=(process.stdout, 'STDOUT') )
        stderr_thread = threading.Thread( target = self.read_output, args=(process.stderr, 'STDERR') )
        stdout_thread.start()
        stderr_thread.start()
        process.wait()
        stdout_thread.join()
        stderr_thread.join()
        
    def windowsService(self):
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'mosquitto.exe'], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            pass
        os.system('''start "" "C:\Program Files\mosquitto\mosquitto.exe" -v -c "C:\Program Files\mosquitto\MosConfGreg.conf"''')

        java = 'C:/Users/PROGregory/.jdks/corretto-17.0.6/bin/java.exe'
        basePath = '''C:/Users/PROGregory/Documents'''
        if self.PRODUCTION:
            java = 'java'
            basePath = 'C:/Users/Mindtrap/Documents'
        cmd = f'''{java} -Dfile.encoding=UTF-8 -jar {basePath}/Github/agent_factory_services/target/{JAR_FILE_NAME}'''
        return cmd
    
    def linuxService(self):
        #print(os.getenv("JAVA_HOME"))
        java = '/usr/lib/jvm/java-17-openjdk-amd64/bin/java'
        #java = 'java'
        extraParam = ''
        cmd = f'''{java} -Dfile.encoding=UTF-8 -DDB_USER=pavlos -DDB_PASSWORD=mindtr@p -jar /home/agentfactory/Documents/Github/agent_factory_services/target/{JAR_FILE_NAME}'''
        return cmd

    def main(self):        
        self.setupLogger(logging.DEBUG)
        cmd = None
        if getPlatform()=='windows':
            cmd = self.windowsService()
        else:
            self.stopSubprocess()
            cmd = self.linuxService()

        self.runSubproccess(cmd)
        self.logger.critical("[-----------------SELF--------------] Java broke completely , restarting again!")
        self.restart()


def main(args):
    options = parser(args)
    DELAY = int(options.delay)
    RESTART_AFTER_ERROR = options.restart
    print(f"SMART-RESTART:{bool(RESTART_AFTER_ERROR)}")
    if DELAY!=0:
        print(f"Booting in {DELAY} seconds...")
        time.sleep(DELAY)
    theMain = myMain()


if __name__ == '__main__':
  sys.exit(main(sys.argv))


