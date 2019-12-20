from copy import deepcopy
import pandas as pd
import numpy as np

from  model import cnn_model
from go import Go
from go import BLACK
from gui import start_game


class GameGo(Go):
    def __init__(self, N):
        super().__init__(N)

    def play_one_move(self):
        # only one empty tile, stop game
        if len(self.empty_tiles) == 1:
            return False

        # AI is the black stone
        board = self.get_board_2d()
        possible_layouts = []
        for i in range(self.N):
            for j in range(self.N):
                if board[i][j] == 0:
                    layout = deepcopy(board)
                    layout[i][j] = 1
                    possible_layouts.append({'data': layout, 'idx': i*self.N+j})
        # print (possible_layouts)
        df = pd.DataFrame(possible_layouts)

        prediction = model.predict(np.array(df['data'].values.tolist()).reshape(-1,12,12,1))

        df['score'] = prediction[:,1] - prediction[:,2] # the score for black winning the game

        # selected_idx = df.iloc[df['score'].idxmax()]['idx']
        # print (r)

        df = df.sort_values(by=['score'], ascending=False)
        sorted_idx = list(df['idx'])

        for idx in sorted_idx:
            success = self.place_stone(idx, BLACK)
            if success:
                return True

        # all of the idx selection not possible, return False
        return False


N = 12   # the model is trained for 12*12 board

model = cnn_model()
model.load_weights('save/weights02.h5')

go = GameGo(N)
start_game(go)
