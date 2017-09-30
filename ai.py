import model
import math
from copy import deepcopy


def takeChecker(x,y, board):
    board[x,y].checker = None

class Move():
    def __init__(self,checker, piece, type):
        self.checker = checker
        self.piece = piece
        self.type = type
        self.distance = 1


def checkNeighbor(x, y, px, py,up=False,down=False,dir=-1):
    results = []
    if up==False:
        if (x == px + 1 and y == py + 1):
            # South_West
            results.append(0)
            if dir == 0:
                results = [0]
                return results
        if (x == px - 1 and y == py + 1):
            # South_East
            results.append(1)
            if dir == 1:
                results = [1]
                return  results
    if down:
        if results == []:
            results.append(-1)
        return results
    if (x == px + 1 and y == py - 1):
        # North_West
        results.append(2)
        if dir == 2:
            results = [2]
            return results
    if (x == px - 1 and y == py - 1):
        # North_East
        results.append(3)
        if dir == 3:
            results = [3]
            return results
    if results == []:
        results.append(-1)
    return results

def findMoves(board, color):
    moves = []
    for piece in board.flat:
        if piece.checker is None or piece.checker.black != color:
            continue
        options = []
        for new_piece in board.flat:
            if color == True or piece.checker.king:
                dir = checkNeighbor(new_piece.x/62.5,new_piece.y/62.5,piece.x/62.5,piece.y/62.5,down=True)
            if color == False or piece.checker.king:
                dir = checkNeighbor(new_piece.x/62.5,new_piece.y/62.5,piece.x/62.5,piece.y/62.5,up=True)
            if dir[0] != -1:
                options.append(new_piece)

        for option in options:
            if option.checker == None:
                moves.append(Move(piece.checker, option, "Move"))
    return moves

def findJumps(board, color):
    jumps = []
    for piece in board.flat:
        if piece.checker is None or piece.checker.black != color:
            continue
        options = []
        dirs = []
        for new_piece in board.flat:
            if new_piece.checker is None or new_piece.checker.black == color:
                continue
            if color == True or piece.checker.king:
                dir = checkNeighbor(new_piece.x/62.5,new_piece.y/62.5,piece.x/62.5,piece.y/62.5,down=True)
            if color == False or piece.checker.king:
                dir = checkNeighbor(new_piece.x/62.5,new_piece.y/62.5,piece.x/62.5,piece.y/62.5,up=True)
            if dir[0] != -1:
                options.append(new_piece)
                dirs.append(dir[0])

        x = 0
        for option in options:
            new_piece = None
            if dirs[x] == 0:
                new_piece = board[int(option.x/62.5)+1,int(option.y/62.5)+1]
            elif dirs[x] == 1:
                new_piece = board[int(option.x/62.5-1),int(option.y/62.5+1)]
            elif dirs[x] == 2:
                new_piece = board[int(option.x/62.5+1),int(option.y/62.5-1)]
            elif dirs[x] == 3:
                new_piece = board[int(option.x/62.5-1),int(option.y/62.5-1)]

            if new_piece.checker == None:
                move = Move(piece.checker, new_piece, "Jump")
                new_board = deepcopy(board)
                new_board[int(new_piece.x / 62.5), int(new_piece.y / 62.5)].checker = new_board[int(piece.x/62.5),int(piece.y/62.5)].checker
                new_board[int(piece.x/62.5),int(piece.y/62.5)].checker.piece = new_board[int(new_piece.x/62.5),int(new_piece.y/62.5)]
                new_board[int(piece.x / 62.5), int(piece.y / 62.5)].checker = None
                new_jumps = findJumps(new_board, color)
                extra_jump = False
                for jump in new_jumps:
                    if jump.checker == piece.checker:
                        extra_jump = True
                        jumps.append(jump)
                if extra_jump == False:
                    jumps.append(move)
            x += 1
    return jumps


