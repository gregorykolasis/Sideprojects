import asyncio 
import json
import serial
from modules.serial_asyncio import create_serial_connection

class mySerial(asyncio.Protocol):

    def __init__(self, loop=None):
        
        self.loop = loop
        self.port = 'COM5'
        self.baud_rate = 115200
        self.buffer = bytearray()
        self.transport = None    
        self.loop.create_task(  self.open_connection()  )

    def IsMasterConnected(self):
        return True

    def connection_made(self, transport):
        self.transport = transport
        asyncio.run_coroutine_threadsafe( self.reset_serial() , self.loop )

    def usb_connection_lost(self):
        self.connection_lost('Error')
        self.loop.create_task(  self.open_connection()  )

    async def open_connection(self):
        loop = self.loop
        while True:
            try:
                _, self.transport = await create_serial_connection(loop, self.usb_connection_lost , lambda: self, self.port, baudrate=self.baud_rate , )
                return self.transport
            except Exception as ex:
                print("Retrying in 1 seconds...")
                await asyncio.sleep(1)  # Wait for 5 seconds before retrying
                print("Unexpected Error:", ex) 

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
        try:
            data = json.loads(message)  
            if data["category"] == "inside":
                self.specialButtons(data["value"])               
            if data["category"] == "outside":
                self.scanOutside(data["value"])                      
            if data["category"] == "gameplay":
                self.checkSerial(data["value"])
            if data["category"] == "emulate":
                self.scanOutside(data["msg"])           
            if data["category"] == "connection-init":
                self.sendSerial("getUptime")
                if self.gamePlaying==True:
                    self.logger.error(f"[Serial]Got connection-init during gameplay , this means that Master Disconnected/Reconnected!")
                    self.sendSerial('start')
            self.logger.info(f"[Serial-Receive]:{data}")
        except Exception as e:
            self.logger.info(f"[Serial-Raw]{message}")

    def serialSend(self,msg):
        self.logger.info(f"[Serial-Send]:{msg}")
        try:
            self.send_serial_data(f"@{msg}#")
        except Exception as e:
            self.logger.error(f"[sendSerial] Error:{e}")
        