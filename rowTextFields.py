import tkinter as tk
import asyncio
import time
import threading
import random
class controller(object):
    def __init__(self, items):
        self.items = items        
    
    def update(self):                       
        for row in self.items:                 
            for i in range (len(row.values)):
                row.values[i].value += int(random.random() * 5)
                row.values[i].value %= 100
            row.render()
        #self.canvas.update_idletasks()
        

class rowCanvas(object):
    def __init__(self, root, row, values):        
        self.values = values
        self.stringvar = tk.StringVar()
        self.stringvar.set(self.getTextString())
        #dont store label        
        label = tk.Label(root, textvariable=self.stringvar,font=FONT,fg='yellow',bg='black')        
        label.pack()
        
    def getTextString(self):
        return " ".join([str(x) for x in self.values])
    
    def render(self):
        self.stringvar.set(self.getTextString())
        
class value(object):
    def __init__(self):
        self.value = 0
    def __str__(self):
        return "%02d" % (self.value)
        
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
    for i in range(600//30):
        row = i
        values = [value() for x in range(30)]
        rowcanvas = rowCanvas(root, row, values)        
        stringVars.append(rowcanvas)

        
    controller = controller(stringVars)
        # Start running the tkinter update() through an asyncio coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tk(root, controller, 0.000))