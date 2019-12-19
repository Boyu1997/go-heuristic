import tkinter
from tkinter import ttk
from tkinter import messagebox
import functools

from go import WHITE, EMPTY


class Application(tkinter.Frame):
    def __init__(self, go, master=None):
        # setup gui
        tkinter.Frame.__init__(self, master)
        self.go = go
        self.master = master
        self.game_buttons = []
        self.pack()
        self.createWidgets()

        # setup style
        s = ttk.Style()
        s.configure('GameBoard.TButton', font='Times 20 bold', height=4, width=1)

    def createWidgets(self):
        # define game board
        board_window = tkinter.Frame(self)
        for piece in self.go.game_board:
            b = ttk.Button(board_window,
                           text=piece.status,
                           style='GameBoard.TButton')
            b['command'] = functools.partial(self.btnClick, piece)
            b.grid(row=piece.x,column=piece.y)
            self.game_buttons.append(b)
        board_window.pack()

        # define function buttons
        self.QUIT = ttk.Button(self, text="QUIT", command=self.master.destroy)
        self.QUIT.pack(side="bottom")

    def refresh_game_board(self):
        for piece, button in zip(self.go.game_board, self.game_buttons):
            button['text'] = piece.status

    def btnClick(self, piece):
        # check valid
        if piece.status == EMPTY:
            # place the piece
            self.go.place_piece(piece.idx, WHITE)
            self.refresh_game_board()

            # place opponent's piece
            self.go.play_one_move()
        else:
            messagebox.showinfo("Error", "A piece can only be placed on an empty tile!")


def start_game(game_board):
    root = tkinter.Tk()
    app = Application(game_board, master=root)
    app.mainloop()
