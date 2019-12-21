import argparse
from copy import deepcopy
import pandas as pd
import numpy as np

from  model.model import cnn_model
from go import Go
from go import BLACK
from gui import start_game


class GameGo(Go):
    def __init__(self, N, model, minimax, pruning):
        super().__init__(N)
        self.model = model
        self.minimax = minimax
        self.pruning = pruning

    def play_one_move(self):
        # only one empty tile, stop game
        if len(self.empty_tiles) == 1:
            return False

        # AI is the black stone
        board = self.get_board_2d()
        possible_layouts = []

        # use minimax to search for a deepth of 2 layers
        if self.minimax:
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

                        if self.pruning:
                            # alpha beta pruning
                            if first_expend:   # always expend the first node
                                prediction = self.model.predict(np.array(possible_sub_layouts).reshape(-1,12,12,1))
                                min_score = min(prediction[:,0] - prediction[:,1])
                                possible_layouts.append({'score': min_score, 'idx': i*self.N+j})
                                first_expend = False
                                max_available = min_score
                            else:   # try to pruning subsequent nodes
                                pointer = 0
                                min_available = 1   # init to largest possible score
                                while pointer < len(possible_sub_layouts):
                                    # because runing neural network prediction is much efficient on batch, we test the edge nodes on batch of 10
                                    prediction = self.model.predict(np.array(possible_sub_layouts[pointer:pointer+10]).reshape(-1,12,12,1))
                                    pointer += 10
                                    this_min_score = min(prediction[:,0] - prediction[:,1])
                                    min_available = min(this_min_score, min_available)
                                    if min_available < max_available:
                                        break   # pruned
                                possible_layouts.append({'score': min_available, 'idx': i*self.N+j})

                        else:
                            # no pruning
                            prediction = self.model.predict(np.array(possible_sub_layouts).reshape(-1,12,12,1))
                            min_score = min(prediction[:,0] - prediction[:,1])
                            possible_layouts.append({'score': min_score, 'idx': i*self.N+j})
            df = pd.DataFrame(possible_layouts)

        # no minimax search, only use conv model to evaluate all the possible next state
        else:
            for i in range(self.N):
                for j in range(self.N):
                    if board[i][j] == 0:
                        layout = deepcopy(board)
                        layout[i][j] = 1
                        possible_layouts.append({'data': layout, 'idx': i*self.N+j})

            df = pd.DataFrame(possible_layouts)
            prediction = self.model.predict(np.array(df['data'].values.tolist()).reshape(-1,12,12,1))
            df['score'] = prediction[:,0] - prediction[:,1] # the score for black winning the game

        # rank the score
        df = df.sort_values(by=['score'], ascending=False)
        sorted_idx = list(df['idx'])

        for idx in sorted_idx:
            success = self.place_stone(idx, BLACK)
            if success:
                return True

        # all of the idx selection not possible, return False
        return False




def main(args):
    N = 12   # the model is trained for 12*12 board

    model = cnn_model()
    model.load_weights('model/save/iteration-00-weights.hdf5')   # load the best model

    go = GameGo(N, model, args.minimax, args.pruning)
    start_game(go)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # model config
    parser.add_argument('--minimax',
        action='store_true',
        help='use minimax search')
    parser.add_argument('--pruning',
        action='store_true',
        help='use alpha-beta pruning')

    args, unparsed = parser.parse_known_args()
    if len(unparsed) != 0:
        raise SystemExit('Unknown argument: {}'.format(unparsed))
    if args.pruning == True and args.minimax == False:
        raise SystemExit('Pruning can only be used along with minimax')

    main(args)
