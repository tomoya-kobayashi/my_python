import tkinter
import tkinter.ttk

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('tkinter canvas trial')
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start_x = tkinter.StringVar()
        self.start_y = tkinter.StringVar()
        self.current_x = tkinter.StringVar()
        self.current_y = tkinter.StringVar()
        self.stop_x = tkinter.StringVar()
        self.stop_y = tkinter.StringVar()

        self.label_description = tkinter.ttk.Label(self, text='Mouse position')
        self.label_description.grid(row=0, column=1)
        self.label_start_x = tkinter.ttk.Label(self, textvariable=self.start_x)
        self.label_start_x.grid(row=1, column=1)
        self.label_start_y = tkinter.ttk.Label(self, textvariable=self.start_y)
        self.label_start_y.grid(row=2, column=1)
        self.label_current_x = tkinter.ttk.Label(self, textvariable=self.current_x)
        self.label_current_x.grid(row=3, column=1)
        self.label_current_y = tkinter.ttk.Label(self, textvariable=self.current_y)
        self.label_current_y.grid(row=4, column=1)
        self.label_stop_x = tkinter.ttk.Label(self, textvariable=self.stop_x)
        self.label_stop_x.grid(row=5, column=1)
        self.label_stop_y = tkinter.ttk.Label(self, textvariable=self.stop_y)
        self.label_stop_y.grid(row=6, column=1)

        self.test_canvas = tkinter.Canvas(self, bg='lightblue', width=300, height=300, highlightthickness=0)
        self.test_canvas.grid(row=0, column=0, rowspan=7)
        self.test_canvas.bind('<ButtonPress-1>', self.start_pickup)
        self.test_canvas.bind('<B1-Motion>', self.pickup_position)
        self.test_canvas.bind('<ButtonRelease-1>', self.stop_pickup)

    def start_pickup(self, event):
        self.start_x.set('x : ' + str(event.x))
        self.start_y.set('y : ' + str(event.y))
        self.stop_x.set('')
        self.stop_y.set('')

    def pickup_position(self, event):
        self.current_x.set('x : ' + str(event.x))
        self.current_y.set('y : ' + str(event.y))

    def stop_pickup(self, event):
        self.stop_x.set('x : ' + str(event.x))
        self.stop_y.set('y : ' + str(event.y))

root = tkinter.Tk()
app = Application(master=root)
app.mainloop()