import random
import numpy as np

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


for i in range(1000):
    go = GoSimulate(9)
    next_move = True
    color = BLACK
    move_count = 0
    while next_move:
        next_move = go.play_one_move(color)
        color = next_color(color)
        move_count += 1
        if move_count == 1000:
            raise RecursionError('Max simulating stepts reached')
    score = go.score()
    print (score)
