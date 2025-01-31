import asyncio 
import sys
import threading
import time
import queue

class myKeyboard():

    def __init__(self, loop=None):
        
        self.loop = loop
        self.loop.create_task(  self.Keyboard()  )

    readyCommand = False

    def checkKeyboard(self,input_queue):
        while True:
            input_queue.put(sys.stdin.read(1))

    async def readKeyboard(self):
        input_queue = queue.Queue()
        input_thread = threading.Thread(target = self.checkKeyboard, args=(input_queue,) )
        input_thread.daemon = True
        input_thread.start()
        parsingWord = False
        word = ''
        while True:
            if not input_queue.empty():
                while not input_queue.empty():
                    parsingWord = True
                    char = input_queue.get()
                    hex = char.encode('utf-8').hex()   
                    if hex == '0a':
                        break
                    else:
                        word += char
            else:
                if parsingWord:
                    #print(f"[Got]This->:{word}")
                    readyCommand = True
                    self.sendSerial(word)
                    word = ''
                    parsingWord = False                 
            await asyncio.sleep(0.1)  

    async def Keyboard(self):
        await self.readKeyboard()      