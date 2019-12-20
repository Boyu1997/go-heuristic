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
        for stone in self.go.game_board:
            b = ttk.Button(board_window,
                           text=stone.status,
                           style='GameBoard.TButton')
            b['command'] = functools.partial(self.btnClick, stone)
            b.grid(row=stone.x,column=stone.y)
            self.game_buttons.append(b)
        board_window.pack()

        # define function buttons
        self.SCORE = ttk.Button(self, text="SCORE", command=self.score)
        self.SCORE.pack(side="bottom")
        self.QUIT = ttk.Button(self, text="QUIT", command=self.master.destroy)
        self.QUIT.pack(side="bottom")

    def refresh_game_board(self):
        for stone, button in zip(self.go.game_board, self.game_buttons):
            button['text'] = stone.status

    def score(self):
        score = self.go.score()
        self.refresh_game_board()
        print (score)

    def btnClick(self, stone):
        # check valid
        if stone.status == EMPTY:
            # place the stone
            success = self.go.place_stone(stone.idx, WHITE)
            if success:
                self.refresh_game_board()

                # place opponent's stone
                success = self.go.play_one_move()
                if not success:   # no move valid move
                    messagebox.showinfo("Info", "End of game!")
                    score = self.go.score()
                    print (score)

                self.refresh_game_board()
            else:
                messagebox.showinfo("Error", "Ko rule violation!")

        else:
            messagebox.showinfo("Error", "A stone can only be placed on an empty tile!")


def start_game(game_board):
    root = tkinter.Tk()
    app = Application(game_board, master=root)
    app.mainloop()
