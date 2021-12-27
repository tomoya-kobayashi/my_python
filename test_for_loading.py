from tkinter import *
import sys
from threading import Thread
import time
class Conversor(Tk):
    def __init__(self):
        super().__init__()
        self.loaded=False
        self.geometry('400x300')
        Thread(target=self.loading_screen).start()
        label=Label(self)
        label.pack()
        for i in range(10000): #Increase load time
            label['text']+=str(i)
            if i%100==0:
                label['text']+='\n'
    def loading_screen(self):
        idx=0
        while not self.loaded:
            chars= r"/—\|"
            sys.stdout.write('\r'+'loading...'+chars[idx])
            sys.stdout.flush()
            if idx==len(chars)-1:
                idx=0
            else:
                idx+=1
            time.sleep(.1)
        else:
            sys.stdout.write('\nloaded')
    def start(self):
        self.loaded=True
        self.mainloop()
if __name__=='__main__':
    conversor=Conversor()
    conversor.start()