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
        return chain, reach

    def attempt_capture(self, idx):
        chain, reach = self.find_chain_and_reach(idx)

        # if no empty reach, capture
        if not any(self.game_board[r].status == EMPTY for r in reach):
            self.bulk_update(chain, EMPTY)
            # return the number of stones captured
            return len(chain)

        # return 0 stone captured
        return 0

    def check_ko(self, idx, my_color):
        n_status = {self.game_board[n].status for n in self.game_board[idx].neighbors}

        # true only if resounded by opponent color
        if len(n_status) == 1:
            ko_status = list(n_status)[0]
            if ko_status != EMPTY and ko_status != my_color:
                return True

        return None

    def bulk_update(self, idx_list, status):
        if status == EMPTY:
            for idx in idx_list:
                self.game_board[idx].status = EMPTY
                self.empty_tiles.add(idx)
        else:
            for idx in idx_list:
                self.game_board[idx].status = status
                self.empty_tiles.remove(idx)

    def place_stone(self, placed_idx, my_color):
        # check ko rule part 1
        is_ko = self.check_ko(placed_idx, my_color)
        if is_ko and self.last_ko and placed_idx in self.game_board[self.last_ko].neighbors:
            return False
        self.last_ko = None

        # place the stone
        self.game_board[placed_idx].status = my_color
        self.empty_tiles.remove(placed_idx)

        # init for checks
        my_color = self.game_board[placed_idx].status
        opp_color = WHITE if my_color == BLACK else BLACK
        my_stones = []
        opp_stones = []

        # find positions to check
        for n in self.game_board[placed_idx].neighbors:
            if self.game_board[n].status == my_color:
                my_stones.append(n)
            elif self.game_board[n].status == opp_color:
                opp_stones.append(n)

        # check if captures opponent
        opp_captured_count = 0
        for idx in opp_stones:
            opp_captured_count += self.attempt_capture(idx)

        # check ko rule part 2
        if is_ko:
            if opp_captured_count == 1:
                self.last_ko = placed_idx   # set as last_ko to avoid captured in next play
            elif self.attempt_capture(placed_idx) == 1:
                return False   # return false for invalid operation

        # check if captured by opponent
        for idx in my_stones:
            self.attempt_capture(idx)

        # valid, return True
        return True

    def count(self, color):
        count = 0
        for stone in self.game_board:
            if stone.status == color:
                count += 1
        return count

    def score(self):
        '''
        assume all dead stones are taken
        idealy, we want a method to determine which chain of stone is dead
        '''

        while len(self.empty_tiles):
            idx = self.empty_tiles.pop()
            self.empty_tiles.add(idx)
            spaces, borders = self.find_chain_and_reach(idx)
            border_colors = set([self.game_board[b].status for b in borders])
            if len(border_colors) == 1:
                if BLACK in border_colors:
                    self.bulk_update(spaces, BLACK)
                else:
                    self.bulk_update(spaces, WHITE)
            else:
                self.bulk_update(spaces, '?')

        return self.count(BLACK) - self.count(WHITE)

    def play_one_move(self):
        idx = random.sample(self.empty_tiles, 1)[0]
        success = self.place_stone(idx, BLACK)
        if not success:
            self.play_one_move()
