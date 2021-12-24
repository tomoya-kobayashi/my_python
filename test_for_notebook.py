from tkinter import *
import tkinter.ttk as ttk

class NotebookEventSample(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.create_widgets()
        self.pack()

    def create_widgets(self):
        note = ttk.Notebook(self)
        note.pack()
        self.note = note
        note0 = ttk.Frame(note,width=300,height=300)
        note1 = ttk.Frame(note,width=300,height=300)
        note2 = ttk.Frame(note,width=300,height=300)
        note.add(note0,text="note0",state="normal")
        note.add(note1,text="note1",state="normal")
        note.add(note2,text="note2",state="normal")
        note.bind("<<NotebookTabChanged>>",self.getNoteName)
        self.label = ttk.Label(self,text="none")
        self.label.pack()

    def getNoteName(self,event):
        note =event.widget
        self.label["text"]=note.tab(note.select(),"text")


if __name__ == '__main__':
    master = Tk()
    master.title("NotebookEventSample")
    master.geometry("400x400")
    NotebookEventSample(master)
    master.mainloop()