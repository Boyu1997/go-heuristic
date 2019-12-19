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

    def find_chain_and_reach(self, start_idx):
        color = self.game_board[start_idx].status
        chain = set([start_idx])
        reach = set()
        frontier = [start_idx]
        while frontier:
            idx = frontier.pop()
            chain.add(idx)
            for n in self.game_board[idx].neighbors:
                if self.game_board[n].status == color and not n in chain:
                    frontier.append(n)
                elif self.game_board[n].status != color:
                    reach.add(n)
        print (start_idx, "chain", chain, "reach", reach)
        return chain, reach

    def attempt_capture(self, idx):
        chain, reach = self.find_chain_and_reach(idx)

        # if no empty reach, capture
        if not any(self.game_board[r].status == EMPTY for r in reach):
            for idx in chain:
                self.game_board[idx].status = EMPTY

    def place_piece(self, idx, new_status):
        # update color
        self.game_board[idx].status = new_status

        # init for checks
        my_color = self.game_board[idx].status
        opp_color = WHITE if my_color == BLACK else BLACK
        my_pieces = []
        opp_pieces = []

        # find positions to check
        for n in self.game_board[idx].neighbors:
            if self.game_board[n].status == my_color:
                my_pieces.append(n)
            elif self.game_board[n].status == opp_color:
                opp_pieces.append(n)

        print (my_pieces)
        print (opp_pieces)
        # check if captures opponent
        for idx in opp_pieces:
            self.attempt_capture(idx)

        # check if captured by opponent
        for idx in my_pieces:
            self.attempt_capture(idx)

    def play_one_move(self):
        pass
