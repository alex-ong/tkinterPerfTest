import tkinter as tk
import asyncio
import time
import threading
import random

class controller(object):
    def __init__(self, canvas, items):
        self.canvas = canvas
        self.items = items
        
    
    def update(self):
        #noncached upate
        '''
        for item in self.items:                 
            number = int(canvas.itemcget(item[0],'text'))
            number += 1
            number %= 100
            canvas.itemconfigure(item[0],text=(str(number)))            
        '''
        #cached update
        
        for item in self.items:                 
            item[1] += int(random.random() * 5)
            item[1] %= 100
            canvas.itemconfigure(item[0],text=(str(item[1])))            
        

    
GUI_REFRESH = 0.01
async def run_tk(root, controller, interval=GUI_REFRESH):   
    try:
        startTime = time.time()
        count = 1000
        while count > 0:
            # update gui            
            root.update()      
 
            # update logic if required.            
            controller.update()            
            
            #await asyncio.sleep(interval)
            count -= 1
    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise     
    endTime = time.time()
    print ("TotalTime:" + str(endTime - startTime))
    print ("time/frame" + str((endTime - startTime)/1000)) 
            
FONT = ("Consolas", 16)

if __name__ == '__main__':    
    root = tk.Tk()
    stringVars = []
    canvas = tk.Canvas(root, width=1000, height = 800, background='black')
    for i in range(600):
        row = i // 30
        column = i % 30
        text_id = canvas.create_text(column*30,row*30,anchor="nw",text="00", font=FONT, fill='yellow')
        stringVars.append([text_id, 0])
    canvas.pack()
        
    controller = controller(canvas,stringVars)
        # Start running the tkinter update() through an asyncio coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tk(root, controller, 0.000))