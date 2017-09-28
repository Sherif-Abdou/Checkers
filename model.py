import numpy

class Piece():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.center = [x+25, y+25]
        self.checker = None

class Checker():
    def __init__(self):
        self.alive = True
        self.king = False
        self.piece = None
        self.black = False
        self.circle = None
    def moveChecker(self, newPiece):
        self.piece = newPiece
        self.circle.move(newPiece.center[0],newPiece.center[1])


board = numpy.empty((8,8), dtype=Piece)
checkers = []
piece_offset=False


def addChecker(x, y):
    if y == 3 or y == 4:
        return
    checker = Checker()
    if y < 4:
        checker.black = True
    checker.piece = board[x,y]
    board[x,y].checker = checker
    checkers.append(checker)

for x in range(0,8):
    if x%2 == 1:
        piece_offset = True
    else:
        piece_offset = False
    for y in range(0,8):
        piece = Piece(x*62.5,y*62.5)
        board[x,y] = piece
        if (x%2 == 0 or y%2 == 0) and (piece_offset == True):
            addChecker(x,y)
        elif (x%2 == 1 or y%2 == 1) and (piece_offset == False):
            addChecker(x,y)
#print(board)