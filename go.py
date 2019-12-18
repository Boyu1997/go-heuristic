WHITE, BLACK, EMPTY = '○', '●', ' '

class GoPiece():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = EMPTY
