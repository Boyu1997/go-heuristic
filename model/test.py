import sys
import random
import json
from tqdm import tqdm
import numpy as np
from copy import deepcopy
import pandas as pd
from keras.backend import reshape

from model import cnn_model

# import from files in parent directory
sys.path.append("..")
from go import Go
from go import BLACK, WHITE, EMPTY
sys.path.append("/model")




class GoSimulate(Go):
    def __init__(self, N):
        super().__init__(N)

    def play_one_move(self, model, color):
        # only one empty tile, stop game
        if len(self.empty_tiles) == 1:
            return False

        if color == BLACK:
            board = self.get_board_2d()
            possible_layouts = []
            for i in range(self.N):
                for j in range(self.N):
                    if board[i][j] == 0:
                        layout = deepcopy(board)
                        layout[i][j] = 1
                        possible_layouts.append({'data': layout, 'idx': i*self.N+j})

            df = pd.DataFrame(possible_layouts)
            prediction = model.predict(np.array(df['data'].values.tolist()).reshape(-1,12,12,1))
            df['score'] = prediction[:,0] - prediction[:,1] # the score for black winning the game

            df = df.sort_values(by=['score'], ascending=False)
            sorted_idx = list(df['idx'])

            for idx in sorted_idx:
                success = self.place_stone(idx, color)
                if success:
                    return True

            # all of the idx selection not possible, return False
            return False

        # continue otherwise
        else:
            idx = random.sample(self.empty_tiles, 1)[0]
            success = self.place_stone(idx, color)
            if not success:
                try:
                    self.place_stone(idx, color)
                except RecursionError:
                    return False
            return True

def next_color(color):
    if color == BLACK:
        return WHITE
    else:
        return BLACK



def test(model_path, test_count=100):

    model = cnn_model()
    model.load_weights(model_path)

    result_satistic = {'model_win': 0, 'model_loss': 0, 'draw':0}   # with respect to BLACK
    simulation_data = []

    for _ in tqdm(range(test_count)):
        go = GoSimulate(12)

        next_move = True
        color = BLACK
        move_count = 0
        game_steps = []

        while next_move:
            next_move = go.play_one_move(model, color)
            color = next_color(color)
            game_steps.append(go.get_board_2d())
            move_count += 1
            if move_count == 10000:
                raise RecursionError('Max simulating stepts reached')

        score = go.score()
        if score > 0:
            result_satistic['model_win'] += 1
            result = 1
        elif score < 0:
            result_satistic['model_loss'] += 1
            result = 2
        elif score == 0:
            result_satistic['draw'] += 1
            result = 0

        for s in game_steps:
            simulation_data.append({'data': s, 'label': result})

    print ("Test result (model player vs random player):")
    print (result_satistic)
