import numpy
import uuid
import ai

class Piece():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.center = [x + 25, y + 25]
        self.checker = None


class Checker():
    def __init__(self):
        self.alive = True
        self.king = False
        self.x = None
        self.y = None
        self.black = False
        self.circle = None
        self.id = None


def moveChecker(checker, piece):
    piece.checker = checker
    checker.circle.move(piece.center[0], piece.center[1])

board = numpy.empty((8, 8), dtype=Piece)
checkers = []
piece_offset = False


def addChecker(x, y):
    if y == 3 or y == 4:
        return
    checker = Checker()
    checker.id = (x, y)
    if y < 4:
        checker.black = True
    checker.x = x
    checker.y = y
    board[x, y].checker = checker
    checkers.append(checker)


for x in range(0, 8):
    if x % 2 == 1:
        piece_offset = True
    else:
        piece_offset = False
    for y in range(0, 8):
        piece = Piece(x * 62.5, y * 62.5)
        board[x, y] = piece
        if (x % 2 == 0 or y % 2 == 0) and (piece_offset == True):
            addChecker(x, y)
        elif (x % 2 == 1 or y % 2 == 1) and (piece_offset == False):
            addChecker(x, y)
            # print(board)


def getFullMove(partial_move):
    moves = ai.findJumps(board, False)
    for move in moves:
        if move.checker.id == partial_move.checker.id and move.piece.x == partial_move.piece.x \
                and move.piece.y == partial_move.piece.y:
            return move
    return None
