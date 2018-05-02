import copy
import pickle
import random
import numpy
import ai



# The board's pieces
class Piece():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.center = [x + 25, y + 25]
        self.checker = None

# Completely copies board for minimax


def copyBoard(origin):
    new_board = copy.deepcopy(origin)
    for piece in board.flat:
        new_board[int(piece.x / 62.5), int(piece.y / 62.5)
                  ] = copy.deepcopy(piece)
        new_board[int(piece.x / 62.5), int(piece.y / 62.5)
                  ].checker = copy.deepcopy(piece.checker)
    return new_board

# A checker on the board


class Checker():
    def __init__(self):
        self.alive = True
        self.king = False
        self.x = None
        self.y = None
        self.black = False
        self.circle = None
        self.id = None
        self.index = None


def moveChecker(checker, piece):
    piece.checker = checker
    checker.circle.move(piece.center[0], piece.center[1])


# The main board of the game
board = numpy.empty((8, 8), dtype=Piece)
checkers = []

def addChecker(x, y):
    if y == 3 or y == 4:
        return
    checker = Checker()
    checker.id = (x, y)
    checker.index = x*8 + (y+1)
    if y < 4:
        checker.black = True
    checker.x = x
    checker.y = y
    board[x, y].checker = checker
    checkers.append(checker)


# Initializes the board
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


def King(board):
    for piece in board.flat:
        if piece.checker is None or piece.checker.king:
            continue
        if (piece.y / 62.5 == 7 and piece.checker.black) or (piece.y / 62.5 == 0 and not piece.checker.black):
            piece.checker.king = True


def getFullMove(partial_move):
    moves = ai.findJumps(board, False) + ai.findMoves(board, False)
    for move in moves:
        if move.checker.id == partial_move.checker.id and move.piece.x == partial_move.piece.x \
                and move.piece.y == partial_move.piece.y:
            return move
    return None


def hasWon(board):
    white_actions = ai.findJumps(board, False) + ai.findMoves(board, False)
    black_actions = ai.findJumps(board, True) + ai.findMoves(board, True)
    if len(white_actions) == 0:
        return -1
    elif len(black_actions) == 0:
        return 1
    else:
        return 0

zobrist_table = numpy.zeros((8, 8, 64))

for i in range(0,8):
    for j in range(0,8):
        for k in range(0,64):
            zobrist_table[i,j,k] = random.randint(0, 1000000)

def moveToHash(move, board, depth):
    hsh = 0
    for piece in board.flat:
        if piece.checker is None:
            continue
        checker = piece.checker
        hsh = hsh ^ int(zobrist_table[int(piece.x/62.5), int(piece.y/62.5), piece.checker.index])
    hsh += hash(str(move.checker.id) + str(move.checker.x) + str(move.checker.y))
    return hsh



class TranspositionTable():
    def __init__(self):
        self.hashtable = {}
            
    def insert(self, move, nboard, depth):
        index = moveToHash(move, nboard, depth)
        self.hashtable[index] = move.weight
    
    def search(self, move, nboard, depth):
        index = moveToHash(move, nboard, depth)
        return self.hashtable[index]
    def save(self):
        save_file = open('save.dat', 'wb')
        pickle.dump(self.hashtable, save_file)
        save_file.close()

ttable = TranspositionTable()

