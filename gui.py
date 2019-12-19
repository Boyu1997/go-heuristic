import tkinter
from tkinter import ttk
import functools

from go import GoPiece
from go import WHITE


class Application(tkinter.Frame):
    def __init__(self, game_board, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.game_board = game_board
        # self.board_buttons = []
        self.pack()
        self.createWidgets()

        # setup style
        s = ttk.Style()
        s.configure('GameBoard.TButton', font='Times 20 bold', height=4, width=1)

    def createWidgets(self):

        # define game board
        board_window = tkinter.Frame(self)
        for piece in self.game_board:
            b = ttk.Button(board_window,
                           text=piece.status,
                           style='GameBoard.TButton')
            b['command'] = functools.partial(self.btnClick, piece, b)
            b.grid(row=piece.x,column=piece.y)
        board_window.pack()

        # define function buttons
        self.QUIT = ttk.Button(self, text="QUIT", command=self.master.destroy)
        self.QUIT.pack(side="bottom")

    def btnClick(self, piece, button):
        piece.status = WHITE
        button['text'] = WHITE


def start_game(game_board):
    root = tkinter.Tk()
    app = Application(game_board, master=root)
    app.mainloop()
