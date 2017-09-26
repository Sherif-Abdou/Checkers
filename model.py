import numpy

class Piece():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.center = [x+31.25, y+20]
        self.checker = None

class Checker():
    def __init__(self):
        self.alive = True
        self.king = False
        self.piece = None
        self.black = False
        self.circle = None

board = numpy.empty((8,10), dtype=Piece)
checkers = []
piece_offset=False


def addChecker(x, y):
    if y == 4 or y == 5:
        return
    checker = Checker()
    if y < 5:
        checker.black = True
    checker.piece = board[x,y]
    board[x,y].checker = checker
    checkers.append(checker)

for x in range(0,8):
    if x%2 == 1:
        piece_offset = True
    else:
        piece_offset = False
    for y in range(0,10):
        piece = Piece(x*62.5,y*50)
        board[x,y] = piece
        if (x%2 == 0 or y%2 == 0) and (piece_offset == True):
            addChecker(x,y)
        elif (x%2 == 1 or y%2 == 1) and (piece_offset == False):
            addChecker(x,y)
#print(board)