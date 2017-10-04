import model
import math
import graphics
import view
from copy import deepcopy, copy
import sys

def takeChecker(x, y, board):
    board[x, y].checker = None


class Move():
    def __init__(self, checker, piece, type):
        self.checker = checker
        self.piece = piece
        self.type = type
        self.distance = 1
        self.weight = None
        self.origon = None
        self.jumped = []

    def apply(self, board):
        checker_x = self.checker.x
        checker_y = self.checker.y
        new_x = self.piece.x / 62.5
        new_y = self.piece.y / 62.5
        self.checker.x = board[int(new_x), int(new_y)].x/62.5
        self.checker.y = board[int(new_x), int(new_y)].y/62.5
        board[int(checker_x), int(checker_y)].checker = None
        board[int(new_x), int(new_y)].checker = self.checker

        for piece in self.jumped:
            # board[int(piece.x / 62.5), int(piece.y / 62.5)].checker.circle.undraw()
            board[int(piece.x/62.5),int(piece.y/62.5)].checker = None
        # self.checker.circle = graphics.Circle(graphics.Point(self.piece.center[0],self.piece.center[1]), 15)
        # if self.checker.black:
        #     self.checker.circle.setFill("Black")
        # elif not self.checker.black:
        #     self.checker.circle.setFill("White")
        # self.checker.circle.draw(view.win)
        return board


def checkNeighbor(x, y, px, py, up=False, down=False, dir=-1):
    results = []
    if up == False:
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
                return results
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
                dir = checkNeighbor(new_piece.x / 62.5, new_piece.y / 62.5, piece.x / 62.5, piece.y / 62.5, down=True)
            if color == False or piece.checker.king:
                dir = checkNeighbor(new_piece.x / 62.5, new_piece.y / 62.5, piece.x / 62.5, piece.y / 62.5, up=True)
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
                dir = checkNeighbor(new_piece.x / 62.5, new_piece.y / 62.5, piece.x / 62.5, piece.y / 62.5, down=True)
            if color == False or piece.checker.king:
                dir = checkNeighbor(new_piece.x / 62.5, new_piece.y / 62.5, piece.x / 62.5, piece.y / 62.5, up=True)
            if dir[0] != -1:
                options.append(new_piece)
                dirs.append(dir[0])

        x = 0
        for option in options:
            new_piece = None
            if option.x / 62.5 == 0 or option.x / 62.5 == 7 or option.y/62.5 == 0 or option.y/62.5 == 7:
                continue
            if dirs[x] == 0:
                new_piece = board[int(option.x / 62.5) + 1, int(option.y / 62.5) + 1]
            elif dirs[x] == 1:
                new_piece = board[int(option.x / 62.5 - 1), int(option.y / 62.5 + 1)]
            elif dirs[x] == 2:
                new_piece = board[int(option.x / 62.5 + 1), int(option.y / 62.5 - 1)]
            elif dirs[x] == 3:
                new_piece = board[int(option.x / 62.5 - 1), int(option.y / 62.5 - 1)]

            if new_piece.checker == None:
                move = Move(piece.checker, new_piece, "Jump")
                move.jumped.append(option)
                new_board = deepcopy(board)
                new_board[int(new_piece.x / 62.5), int(new_piece.y / 62.5)].checker = new_board[
                    int(piece.x / 62.5), int(piece.y / 62.5)].checker
                new_board[int(piece.x / 62.5), int(piece.y / 62.5)].checker = None
                new_jumps = findJumps(new_board, color)
                extra_jump = False
                for jump in new_jumps:
                    if jump.checker.id == piece.checker.id:
                        extra_jump = True
                        move.jumped.append(option)
                        jump.checker = piece.checker
                        jumps.append(jump)
                if extra_jump == False:
                    jumps.append(move)
            x += 1
    return jumps


def weighBoard(board):
    white_moves = findMoves(board, False) + findJumps(board, False)
    black_moves = findMoves(board, True) + findJumps(board, True)
    for move in white_moves:
        if doesMoveProtect(board, move, False):
            move.weight = 4
        elif doesMoveKing(board, move, False):
            move.weight = 6
        elif move.type == "Move":
            move.weight = 0
        elif move.type == "Jump":
            move.weight = 100 + move.distance - 1

    for move in black_moves:
        if doesMoveProtect(board, move, True):
            move.weight = -4
        elif doesMoveKing(board,move, True):
            move.weight = -6
        elif move.type == "Move":
            move.weight = 0
        elif move.type == "Jump":
            move.weight = -100 - move.distance + 1

    return (white_moves, black_moves)

def doesMoveProtect(board, move, color):
    enemy_jumps = findJumps(board, not color)
    for jump in enemy_jumps:
            if move.piece.x == jump.piece.x and move.piece.y == jump.piece.y:
                return True
    return False

def doesMoveKing(board, move, color):
    if color:
        if move.piece.x/62.5 == 7:
            return True
    elif not color:
        if move.piece.x/62.5 == 0:
            return True

def minimax(depth, color, board, h=2):
    white_moves = weighBoard(board)[0]
    black_moves = weighBoard(board)[1]
    if depth == h:
        if color:
            # Min
            min = None
            for move in white_moves:
                if min == None:
                    min = move
                elif min.weight > move.weight:
                    min = move
            return min
        else:
            # Max
            max = None
            for move in black_moves:
                if max == None:
                    max = move
                elif max.weight < move.weight:
                    max = move
            return max
    if color:
        # Min
        for move in black_moves:
            if move.type == "Jump":
                return move
        max = []
        for move in white_moves:
            print(sys.getrecursionlimit())
            copy = deepcopy(board)
            max.append(minimax(depth + 1, False, move.apply(copy)))

        min = None
        x = 0
        y = 0
        for move in max:
            if move.type == "Jump":
                return move
            if min == None or min.weight > move.weight:
                min = move
                y = x
            x += 1
        return black_moves[y]
    else:
        # Max
        min = []
        for move in black_moves:
            min.append(minimax(depth + 1, True, move.apply(deepcopy(board))))
        max = None
        x = 0
        y = 0
        for move in min:
            if move.type == "Jump":
                return move
            if max == None or max.weight < move.weight:
                max = move
                y = x
            x += 1
        return white_moves[y]
