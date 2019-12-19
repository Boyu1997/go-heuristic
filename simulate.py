import random
import numpy as np
import json

from go import Go
from go import BLACK, WHITE, EMPTY


class GoSimulate(Go):
    def __init__(self, N):
        super().__init__(N)

    def play_one_move(self, color):
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


result_satistic = {'win': 0, 'draw':0, 'loss': 0}   # with respect to BLACK
simulation_data = []

for i in range(1000):
    go = GoSimulate(9)

    next_move = True
    color = BLACK
    move_count = 0
    game_steps = []

    while next_move:
        next_move = go.play_one_move(color)
        color = next_color(color)
        game_steps.append(go.get_board_2d())
        move_count += 1
        if move_count == 1000:
            raise RecursionError('Max simulating stepts reached')

    score = go.score()
    if score > 0:
        result_satistic['win'] += 1
        result = 1
    elif score < 0:
        result_satistic['loss'] += 1
        result = 2
    elif score == 0:
        result_satistic['draw'] += 1
        result = 0

    for s in game_steps:
        simulation_data.append({'data': s, 'label': result})


print (result_satistic)
with open('data.json', 'w') as f:
    json.dump(simulation_data, f)
