import subprocess
import re
import os

output = subprocess.run([
    'powershell.exe', 
    '-noprofile', 
    '-executionpolicy',
    '-bypass',
    '-c', 
    'get-eventlog -LogName System | where-object {$_.eventid -eq 1074} | Select-Object -First 1 -ExpandProperty Message '

  ], 
  capture_output=True)

raw = output.stdout.decode('oem')
print(raw)
msg = re.split(r'\n', raw)
typeLastMessage = msg[2]
print(typeLastMessage)
if 'shutdown' in typeLastMessage:
  os.system('shutdown /r /t 0')

#'get-eventlog -LogName System | where-object {$_.eventid -eq 1074} | select -ExpandProperty Message'
#lines_list = re.split(r'\n', raw)
#lastPart = lines_list[3]
#print(f"Line:{lastPart[50:]}")
#LastBootMessage = lines_list[3]
#print(LastBootMessage)
# if 'shutdown.exe' in LastBootMessage:
#   os.system('shutdown /r /t 0')