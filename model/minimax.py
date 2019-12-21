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


pruning = True

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

            # max layer
            max_available = -1   # init to smallest possible score
            first_expend = True
            for i in range(self.N):
                for j in range(self.N):
                    if board[i][j] == 0:
                        layout = deepcopy(board)
                        layout[i][j] = 1

                        # min layer
                        possible_sub_layouts = []
                        for p in range(self.N):
                            for q in range(self.N):
                                if layout[p][q] == 0:
                                    sub_layout = deepcopy(layout)
                                    sub_layout[p][q] = 2
                                    possible_sub_layouts.append(sub_layout)   # we only needs score at this layer

                        if pruning:
                            # alpha beta pruning
                            if first_expend:   # always expend the first node
                                prediction = model.predict(np.array(possible_sub_layouts).reshape(-1,12,12,1))
                                min_score = min(prediction[:,0] - prediction[:,1])
                                possible_layouts.append({'score': min_score, 'idx': i*self.N+j})
                                first_expend = False
                                max_available = min_score
                            else:   # try to pruning subsequent nodes
                                pointer = 0
                                min_available = 1   # init to largest possible score
                                while pointer < len(possible_sub_layouts):
                                    # because runing neural network prediction is much efficient on batch, we test the edge nodes on batch of 10
                                    prediction = model.predict(np.array(possible_sub_layouts[pointer:pointer+10]).reshape(-1,12,12,1))
                                    pointer += 10
                                    this_min_score = min(prediction[:,0] - prediction[:,1])
                                    min_available = min(this_min_score, min_available)
                                    if min_available < max_available:
                                        break   # pruned
                                possible_layouts.append({'score': min_available, 'idx': i*self.N+j})

                        else:
                            # no pruning
                            prediction = model.predict(np.array(possible_sub_layouts).reshape(-1,12,12,1))
                            min_score = min(prediction[:,0] - prediction[:,1])
                            possible_layouts.append({'score': min_score, 'idx': i*self.N+j})



            # select the maxmium score
            df = pd.DataFrame(possible_layouts)
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



model = cnn_model()
model.load_weights('save/iteration-00-weights.hdf5')

result_satistic = {'model_win': 0, 'model_loss': 0, 'draw':0}   # with respect to BLACK
simulation_data = []

for _ in tqdm(range(10)):
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

print ("Minimax test result (model player vs random player):")
print (result_satistic)
