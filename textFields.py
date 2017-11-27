import tkinter as tk
import asyncio
import time
import threading
import random

class controller(object):
    def __init__(self, root, items):
        self.root = root
        self.items = items
    def update(self):
        for item in self.items:
            number = int(item.get())
            number += int(random.random() * 5)
            number %= 100
            item.set(str(number))
            root.update_idletasks()

    
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
    for i in range(600):
        stringVar = tk.StringVar()        
        stringVar.set("1")
        label = tk.Label(root, textvariable=stringVar,width=2,font=FONT,fg='yellow',bg='black')
        label.grid(row=i//30, column=i%30)
        stringVars.append(stringVar)
        
    controller = controller(root, stringVars)
    #root.grid_propagate(False)
        # Start running the tkinter update() through an asyncio coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tk(root, controller, 0.001))