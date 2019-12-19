WHITE, BLACK, EMPTY = '○', '●', ' '

class GoPiece():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = EMPTY

def init_board(N):
    game_board = [GoPiece(i, j) for i in range(N) for j in range(N)]
    return game_board
