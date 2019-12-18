import tkinter
from tkinter import ttk
import functools

from go import GoPiece

class Application(tkinter.Frame):
    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        # setup style
        s = ttk.Style()
        s.configure('BW.TButton', font='Times 20 bold', height=4, width=8)

    def createWidgets(self):
        N = 5


        buttons = tkinter.Frame (self)

        for i in range(N):
            for j in range(N):
                pice = GoPiece(i, j)
                b = ttk.Button(buttons,
                               text=pice.status,
                               style='BW.TButton',
                               command=functools.partial(self.func, pice))
                b.grid(row=i,column=j)

        buttons.pack()

        self.QUIT = ttk.Button(self, text="QUIT", command=root.destroy)
        self.QUIT.pack(side="bottom")

    def func(self, pice):
        print (pice.x, pice.y)

    def say_hi(self):
        print ("hi")

root = tkinter.Tk()
app = Application(master=root)
app.mainloop()
