import sys
import random
import json
from tqdm import tqdm
import numpy as np
import pandas as pd
from copy import deepcopy

from model import cnn_model

# import from files in parent directory
sys.path.append("..")
from go import Go
from go import BLACK, WHITE, EMPTY
sys.path.append("/model")


class GoSimulate(Go):
    def __init__(self, N):
        super().__init__(N)

    def model_play_one_move(self, model, color):
        # only one empty tile, stop game
        if len(self.empty_tiles) == 1:
            return False

        # get all possible next boards
        board = self.get_board_2d()
        possible_layouts = []
        for i in range(self.N):
            for j in range(self.N):
                if board[i][j] == 0:
                    layout = deepcopy(board)
                    layout[i][j] = 1 if color == BLACK else 2   # 1 represents BLACK, 2 represent WHITE
                    possible_layouts.append({'data': layout, 'idx': i*self.N+j})
        df = pd.DataFrame(possible_layouts)
        prediction = model.predict(np.array(df['data'].values.tolist()).reshape(-1,12,12,1))
        df['score'] = prediction[:,0] - prediction[:,1]   # possibility of BLACK winning
        if color == BLACK:
            df = df.sort_values(by=['score'], ascending=False)   # BLACK wants maximize score
        else:
            df = df.sort_values(by=['score'], ascending=True)   # WHITE wants minimize score
        sorted_idx = list(df['idx'])

        # print (color, df[df['idx'] == sorted_idx[0]]['score'])


        for idx in sorted_idx:
            success = self.place_stone(idx, color)
            if success:
                return True

        # all of the idx selection not possible, return False
        return False


    def random_play_one_move(self, color):
        # only one empty tile, stop game
        if len(self.empty_tiles) == 1:
            return False

        # continue otherwise
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


def simulate(simulation_count=100, model_path=None, heuristic_model_iteration=None):
    result_satistic = {'black_win': 0, 'white_win':0, 'draw': 0}
    simulation_data = []

    if model_path:
        model = cnn_model()
        model.load_weights(model_path)
    else:
        model = None

    for i in tqdm(range(simulation_count)):
        go = GoSimulate(12)

        next_move = True
        color = BLACK
        move_count = 0
        game_steps = []

        # heuristic model game play
        if model != None:
            while next_move:
                if move_count < 10:   # start with random game paly, otherwise all games will be the same
                    next_move = go.random_play_one_move(color)
                else:   # after initial random game palys
                    if random.random() > 0.2:   # heuristic game play most of the times
                        next_move = go.model_play_one_move(model, color)
                    else:   # also use random game play sometimes
                        next_move = go.random_play_one_move(color)
                color = next_color(color)
                game_steps.append(go.get_board_2d())
                move_count += 1
                if move_count == 2000:
                    raise RuntimeError('Max stepts in one simulation reached')

        # random game play
        else:
            while next_move:
                next_move = go.random_play_one_move(color)
                color = next_color(color)
                game_steps.append(go.get_board_2d())
                move_count += 1
                if move_count == 2000:
                    raise RuntimeError('Max stepts in one simulation reached')

        score = go.score()
        if score != 0:   # draw is unlikely, ignore draw data
            if score > 0:
                result_satistic['black_win'] += 1
                result = 0
            elif score < 0:
                result_satistic['white_win'] += 1
                result = 1

            # the initial and last stepts have little information, ignore them
            for s in game_steps:
                simulation_data.append({'data': s, 'label': result})
        else:
            result_satistic['draw'] += 1



    # print result
    print (result_satistic)

    # save simulated game play data
    if heuristic_model_iteration != None:
        path = 'data/iteration-{:02d}-data.json'.format(heuristic_model_iteration)
    else:
        path = 'data.json'
    with open(path, 'w') as f:
        json.dump(simulation_data, f)
