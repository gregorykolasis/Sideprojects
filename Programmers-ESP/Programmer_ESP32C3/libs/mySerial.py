import asyncio 
import json
import serial
from modules.serial_asyncio import create_serial_connection

from libs.utils import getPlatform
import numpy as np
import serial.tools.list_ports as port_list  # port finder
import re
import subprocess
from datetime import datetime

class mySerial(asyncio.Protocol):

    def __init__(self, loop=None, openConnection=True, searchPort=True):
        self.loop = loop
        self.baud_rate = 115200
        self.buffer = bytearray()
        self.transport = None    
        if openConnection: 
            self.loop.create_task( self.open_connection(searchPort) )
        
    firstTimeBootedMaster = True

    connected = False
    devices = []
    acceptedPorts = [
        {"type": "description", "value": "CP2102N USB to UART Bridge Controller"},
        {"type": "description", "value": "Silicon Labs CP210x USB to UART Bridge"},
        {"type": "description", "value": "USB Serial Device"},
    ]
    printSearching = True

    def getAllPorts(self):
        devs = []; usb = []
        if getPlatform() == "linux":
            device_re = re.compile(
                b"Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
            df = subprocess.check_output("lsusb")
            for i in df.split(b'\n'):
                if i:
                    info = device_re.match(i)
                    if info:
                        dinfo = info.groupdict()
                        dinfo['bus'] = dinfo.pop('bus')
                        usb.append(dinfo)
        ports = port_list.comports()
        for p in ports:
            if usb:
                for d in usb:
                    hwid = d['id'].decode("utf-8").upper()
                    if (hwid in p.hwid):
                        devs.append( {"device": p.device, "manufacturer": p.manufacturer, "description": p.description, "tag": d["tag"].decode("utf-8"), "path": p.usb_interface_path} )
                        break
            else:
                devs.append( {"device": p.device, "manufacturer": p.manufacturer, "description": p.description, "tag": "", "path": ""} )
        return devs

    async def findCOM(self , strict=True):
        self.port = ""
        self.connected = False
        devs = self.getAllPorts()
        if np.array_equal(devs, self.devices):
            pass
        else:
            self.devices = devs
            for d in devs:
                print(d)
        for p in devs:
            if strict:
                for a in self.acceptedPorts:
                    key = a["type"]
                    try:
                        if a["value"] in p[key]:
                            self.port = p["device"]
                            break
                    except:
                        pass
            else:
                self.port = p["device"]
                break
        await asyncio.sleep(1)
        if self.port != "":
            self.logger.warning(f"[Serial]Found port at:{self.port}")
            self.printSearching = True
            return self.port
        else:
            if self.printSearching == True:
                self.logger.info("[Serial]Searching for Port...")
                self.printSearching = False
            return ""

    def IsMasterConnected(self):
        return True

    def connection_made(self, transport):
        self.transport = transport
        asyncio.run_coroutine_threadsafe( self.reset_serial() , self.loop )

    def usb_connection_lost(self):
        self.connection_lost('Error')
        self.loop.create_task(  self.open_connection()  )

    async def open_connection(self, searchPort = True):
        loop = self.loop
        if searchPort:
            while True:
                self.port = ""
                self.port = await self.findCOM()
                if self.port != "":
                    break
        while True:
            try:
                _, self.transport = await create_serial_connection(loop, self.usb_connection_lost , lambda: self, self.port, baudrate=self.baud_rate , )
                return self.transport
            except Exception as ex:
                print("Retrying in 1 seconds...")
                await asyncio.sleep(1)  # Wait for 5 seconds before retrying
                print("Unexpected Error:", ex) 

    async def close_connection(self):
        if self.transport:
            self.transport.close()  # Close the transport
            self.transport = None
            print("Serial connection closed.")
        else:
            print("No active serial connection to close.")

    def connection_lost(self, exc):
        self.transport = None

    def send_serial_data(self, data):
        if self.transport:
            self.transport.write(data.encode('utf-8'))
        else:
            print("Error: No active serial connection.")

    async def reset_serial(self):
        if not self.transport:
            self.logger.error("Cannot reset serial, no active connection")
            return
        try:
            self.transport.serial.dtr = False
            await asyncio.sleep(0.01)
            self.transport.serial.dtr = True
            self.logger.info("[Serial]Connection reset")
        except serial.SerialException as e:
            self.logger.error(f"[Serial]Connection reset Error: {str(e)}")

    def data_received(self, data):
        try:
            self.buffer.extend(data)
            while b'\n' in self.buffer or b'\r' in self.buffer:
                newline_index = min(self.buffer.index(b'\n') if b'\n' in self.buffer else float('inf'),self.buffer.index(b'\r') if b'\r' in self.buffer else float('inf'))
                line = bytes(self.buffer[:newline_index])
                del self.buffer[:newline_index + 1]
                decoded_data = line.decode('utf-8', 'ignore').strip()
                if decoded_data:
                    #print(f"[Serial] {decoded_data}")  
                    self.handleReceivedData(decoded_data)
        except Exception as e:
            asyncio.run_coroutine_threadsafe(self.open_connection(), self.loop)
            self.logger.error(f"[data_received] Error:{e}")

    def handleReceivedData(self,message):
        now = datetime.now()
        timeNow = now.strftime('%H:%M:%S.%f')[:-3]
        self.logger.info(f"{timeNow} -> {message}")

    def serialSend(self,msg):
        self.logger.info(f"[Serial-Send]:{msg}")
        try:
            msg_ = str(msg).replace("@","").replace("#","")
            self.send_serial_data(f"@{msg_}#")
        except Exception as e:
            self.logger.error(f"[sendSerial] Error:{e}")
        