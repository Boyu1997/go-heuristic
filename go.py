import random

WHITE, BLACK, EMPTY = '○', '●', ' '

class GoStone():
    def __init__(self, x, y, idx):
        self.x = x
        self.y = y
        self.idx = idx
        self.status = EMPTY

class Go():
    def __init__(self, N):
        self.N = N
        self.game_board = [GoStone(i, j, i*N+j) for i in range(N) for j in range(N)]
        self.empty_tiles = set(range(N*N))

        # find neighbors for all stone
        for stone in self.game_board:
            possible_ns = [[stone.x+1, stone.y],
                           [stone.x-1, stone.y],
                           [stone.x, stone.y+1],
                           [stone.x, stone.y-1]]
            stone.neighbors = [n[0]*N + n[1] for n in possible_ns
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
                self.empty_tiles.add(idx)

    def place_stone(self, idx, new_status):
        # place the stone
        self.game_board[idx].status = new_status
        self.empty_tiles.remove(idx)
        print ("empty", self.empty_tiles)

        # init for checks
        my_color = self.game_board[idx].status
        opp_color = WHITE if my_color == BLACK else BLACK
        my_stones = [idx]
        opp_stones = []

        # find positions to check
        for n in self.game_board[idx].neighbors:
            if self.game_board[n].status == my_color:
                my_stones.append(n)
            elif self.game_board[n].status == opp_color:
                opp_stones.append(n)

        print (my_stones)
        print (opp_stones)
        # check if captures opponent
        for idx in opp_stones:
            self.attempt_capture(idx)

        # check if captured by opponent
        for idx in my_stones:
            self.attempt_capture(idx)

    def play_one_move(self):
        idx = random.sample(self.empty_tiles, 1)[0]
        self.place_stone(idx, BLACK)
