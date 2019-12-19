WHITE, BLACK, EMPTY = '○', '●', ' '

class GoPiece():
    def __init__(self, x, y, idx):
        self.x = x
        self.y = y
        self.idx = idx
        self.status = EMPTY

class Go():
    def __init__(self, N):
        self.N = N
        self.game_board = [GoPiece(i, j, i*N+j) for i in range(N) for j in range(N)]

        # find neighbors for all piece
        for piece in self.game_board:
            possible_ns = [[piece.x+1, piece.y],
                           [piece.x-1, piece.y],
                           [piece.x, piece.y+1],
                           [piece.x, piece.y-1]]
            piece.neighbors = [n[0]*N + n[1] for n in possible_ns
                               if n[0]%N == n[0] and n[1] % N == n[1]]

    def place_piece(self, idx, new_status):
        self.game_board[idx].status = new_status

    def play_one_move(self):
        pass
