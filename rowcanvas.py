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
        for row in self.items:                 
            for i in range (len(row.values)):
                row.values[i].value += int(random.random() * 5)
                row.values[i].value %= 100
            row.render()
        

class rowCanvas(object):
    def __init__(self, canvas, row,values):
        self.canvas = canvas
        self.values = values
        
        self.text_id = canvas.create_text(0,row*30,anchor="nw",text=self.getTextString(), font=FONT, fill='yellow')
            
    def getTextString(self):
        return " ".join([str(x) for x in self.values])
    
    def render(self):
        self.canvas.itemconfigure(self.text_id,text=self.getTextString())
        
class value(object):
    def __init__(self):
        self.value = 0
    def __str__(self):
        return "%02d" % (self.value)
        
GUI_REFRESH = 0.01
async def run_tk(root, controller, interval=GUI_REFRESH):   
    try:
        timer = time.time()
        while True:
            # update gui
            newTime = time.time()
            delta = newTime - timer            
                                    
            root.update()      
             
            # update logic if required.
            controller.update()
            
            await asyncio.sleep(interval)
            print (delta)
            timer = newTime
            
    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise     
            
FONT = ("Helvetica", 16)

if __name__ == '__main__':    
    root = tk.Tk()
    stringVars = []
    canvas = tk.Canvas(root, width=1000, height = 800, background='black')
    for i in range(600//30):
        row = i
        values = [value() for x in range(30)]
        rowcanvas = rowCanvas(canvas,row,values)        
        stringVars.append(rowcanvas)
    canvas.pack()
        
    controller = controller(canvas,stringVars)
        # Start running the tkinter update() through an asyncio coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tk(root, controller, 0.001))