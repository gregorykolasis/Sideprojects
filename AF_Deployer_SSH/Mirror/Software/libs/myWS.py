import asyncio 
import json
try:
    import websockets
except ModuleNotFoundError as e:
    import os
    os.system("pip install websockets")

from threading import Timer

from libs.utils import myIP

class myWS:
    def __init__(self, loop=None):
        self.loop = loop

    CLIENTS = []   
    startOnce = True
    firstTimeBootedMaster = True
        
    def IsMasterConnected(self):
        if len(self.CLIENTS)!=0:
            return True
        else:
            return False
        
    async def leSend(self):
        while True:
            self.sendSerial("Test-exchange")
            await asyncio.sleep(1)    

    async def unregister(self,websocket):
        for i, v in enumerate(self.CLIENTS):
            if v["ws"] == websocket:
                self.CLIENTS.remove(v)

    def WsClientConnected(self):
        if self.firstTimeBootedMaster:
            self.logger.warning("============SENDING-RESTART-TO-MASTER===========")
            self.sendSerial("RESTART")  
            self.firstTimeBootedMaster = False          
                
    async def server(self,websocket,path):
        self.CLIENTS.append({"ws": websocket, "clientID": "Unknown"})
        self.WsClientConnected()
        try:
            async for message in websocket:
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
                    # if data["category"] == "testexchange":
                    #     if self.startOnce:
                    #         self.loop.create_task(self.leSend())   
                    #         self.startOnce = False
                    if data["category"] == "connection-init":
                        for i, v in enumerate(self.CLIENTS):
                            if v["ws"] == websocket:
                                self.sendSerial("getUptime")
                                v["clientID"] = data["sender"]
                                if self.gamePlaying==True:
                                    self.logger.error(f"[WS]Got connection-init during gameplay , this means that Master Disconnected/Reconnected!")
                                    self.sendSerial('start')
                                break
                    self.logger.info(f"[WS-Receive]:{data}")
                except Exception as e:
                    self.logger.info(f"[WS]------Exception handler----- error:{e} , message:{message}")
        except websockets.ConnectionClosed as e:
            self.logger.error(f"[websockets.ConnectionClosed] Error:{e}")
        except Exception as e :
            self.logger.error(f"[async for message in websocket:] Error:{e}")    
        finally:
            await self.unregister(websocket)
            
    def startWS(self):
        port = 6789
        result = "Unknown"
        while result != "Success":
            try:
                address = myIP()
                if address != "127.0.0.1":
                    self.logger.info(f"[WS]Starting server at address:{address} , port:{port}")      
                    start_server = websockets.serve(self.server, address, 6789, max_size=None , ping_interval=None) 
                    '''
                        https://websockets.readthedocs.io/en/stable/topics/timeouts.html
                        websockets sends pings at 20 seconds intervals to keep the connection open.
                        It closes the connection if it doesnt get a pong within 20 seconds.
                        You can adjust this behavior with ping_interval and ping_timeout.
                        Setting ping_interval to None disables the whole keepalive and heartbeat mechanism.
                        Setting ping_timeout to None disables only timeouts. This enables keepalive, to keep idle connections open, and disables heartbeat, to support large latency spikes.
                    '''                      
                    self.loop.run_until_complete(start_server)
                    result = "Success"
                else:
                    if result == "Unknown":
                        print(f"[WS]FAIL-IP:{address}")
                    result = "Fail"
            except Exception as e:
                result = "Fail"
                self.logger.error(f"[WS]Error creating server:{e}")

    async def executeMsg(self,msg):
        if len(self.CLIENTS)>0:
            message = json.dumps({"type": "gameplay", "value": msg})
            for i, v in enumerate(self.CLIENTS):  
                try:
                    await v["ws"].send(message)
                    self.logger.info(f"[WS-Send]:{message}")
                except websockets.ConnectionClosed:
                    self.logger.error(f"[WS-Send] Error :{e}")
                    pass

    def examineTask(self,task):
        print(task)

    def sendSerial(self,msg):
        try:
            #asyncio.run(self.executeMsg(msg))
            asyncio.run_coroutine_threadsafe(self.executeMsg(msg), self.loop)  
            '''
            #task = self.loop.create_task(self.executeMsg(msg))
            print(task)
            countdownTimer = Timer(4,self.examineTask,[task]);
            countdownTimer.start()
            '''            
        except Exception as e:
            print(e)
