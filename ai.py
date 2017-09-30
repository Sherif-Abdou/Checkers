import model
import math

class Move():
    def __init__(self,checker, piece, type):
        self.checker = checker
        self.piece = piece
        self.type = type


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
            if color == True:
                dir = checkNeighbor(new_piece.x/62.5,new_piece.y/62.5,piece.x/62.5,piece.y/62.5,down=True)
            if color == False:
                dir = checkNeighbor(new_piece.x/62.5,new_piece.y/62.5,piece.x/62.5,piece.y/62.5,up=True)
            if dir[0] != -1:
                options.append(new_piece)

        for option in options:
            if option.checker == None:
                moves.append(Move(piece.checker, option, "Move"))
    return moves