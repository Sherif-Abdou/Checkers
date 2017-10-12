import model
from copy import deepcopy


def takeChecker(x, y, board):
    board[x, y].checker = None


class Move():
    def __init__(self, checker, piece, type):
        self.checker = checker
        self.piece = piece
        self.type = type
        self.distance = 1
        self.weight = None
        self.jumped = []

    # Applies a move to a given board
    def apply(self, board):
        checker_x = self.checker.x
        checker_y = self.checker.y
        new_x = self.piece.x / 62.5
        new_y = self.piece.y / 62.5
        board[int(checker_x), int(checker_y)].checker = None
        board[int(new_x), int(new_y)].checker = deepcopy(self.checker)
        board[int(new_x), int(new_y)].checker.x = board[int(new_x), int(new_y)].x/62.5
        board[int(new_x), int(new_y)].checker.y = board[int(new_x), int(new_y)].y/62.5

        for piece in self.jumped:
            board[int(piece.x/62.5),int(piece.y/62.5)].checker = None
        return board


# checks if 2 sets of piece positions are cornering each other
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

# Finds the one-step moves a side can make
def findMoves(board, color):
    moves = []
    for piece in board.flat:
        if piece.checker is None or piece.checker.black != color:
            continue
        options = []
        for new_piece in board.flat:
            dirs = []
            if color == True or piece.checker.king:
                dirs.append(checkNeighbor(new_piece.x / 62.5, new_piece.y / 62.5, piece.x / 62.5, piece.y / 62.5, down=True))
            if color == False or piece.checker.king:
                dirs.append(checkNeighbor(new_piece.x / 62.5, new_piece.y / 62.5, piece.x / 62.5, piece.y / 62.5, up=True))
            for direction in dirs:
                if direction[0] != -1:
                    options.append(new_piece)

        for option in options:
            if option.checker == None:
                moves.append(Move(piece.checker, option, "Move"))
    return moves

# Finds Jumps that a side can make
def findJumps(board, color, old=None, depth=0):
    jumps = []
    for piece in board.flat:
        if piece.checker is None or piece.checker.black != color:
            continue
        options = []
        dirs = []
        for new_piece in board.flat:
            dir = []
            if new_piece.checker is None or new_piece.checker.black == color:
                continue
            if color == True or piece.checker.king:
                dir.append(checkNeighbor(new_piece.x / 62.5, new_piece.y / 62.5, piece.x / 62.5, piece.y / 62.5, down=True))
            if color == False or piece.checker.king:
                dir.append(checkNeighbor(new_piece.x / 62.5, new_piece.y / 62.5, piece.x / 62.5, piece.y / 62.5, up=True))
            for direction in dir:
                if direction[0] != -1:
                    options.append(new_piece)
                    dirs.append(direction[0])
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
                new_board = model.copyBoard(board)
                move.apply(new_board)
                if depth < 2:
                    new_jumps = findJumps(new_board, color, option, depth+1)
                    extra_jump = False
                    for jump in new_jumps:
                        if jump.checker.id == piece.checker.id:
                            extra_jump = True
                            jump.jumped.append(option)
                            if old is not None:
                                jump.jumped.append(old)
                            jump.checker = piece.checker
                            jumps.append(jump)
                    if extra_jump == False:
                        jumps.append(move)
            x += 1
    return jumps

# Weighs a board based different types of available moves
def weighBoard(board):
    white_moves = findMoves(board, False) + findJumps(board, False)
    black_moves = findMoves(board, True) + findJumps(board, True)
    for move in white_moves:
        if doesMoveProtect(board, move, False):
            move.weight = 4
        elif enemyJump(board, move, False):
            move.weight = -3
        elif doesMoveEscape(board, move, False):
            move.weight = 3
        elif doesMoveKing(board, move, False):
            move.weight = 6
        elif move.type == "Move":
            move.weight = 0
        elif move.type == "Jump":
            move.weight = 100 + move.distance - 1

    for move in black_moves:
        if doesMoveProtect(board, move, True):
            move.weight = -4
        elif enemyJump(board, move, True):
            move.weight = 3
        elif doesMoveEscape(board, move, True):
            move.weight = -3
        elif doesMoveKing(board,move, True):
            move.weight = -6
        elif move.type == "Move":
            move.weight = 0
        elif move.type == "Jump":
            move.weight = -100 - move.distance + 1

    return (white_moves, black_moves)


# Checks if a move is a suicide run for a checker
# Improves AI significantly
def enemyJump(board, move, color):
    enemy_jumps = findJumps(move.apply(model.copyBoard(board)), not color)
    for jump in enemy_jumps:
        for victim in jump.jumped:
            if victim.checker.id == move.checker.id:
                return True
    return False


# Checks if move is protecting a checker
def doesMoveProtect(board, move, color):
    enemy_jumps = findJumps(board, not color)
    for jump in enemy_jumps:
            if move.piece.x == jump.piece.x and move.piece.y == jump.piece.y:
                return True
    return False

# Checks if a move kings the checker
def doesMoveKing(board, move, color):
    if color:
        if move.piece.x/62.5 == 7:
            return True
    elif not color:
        if move.piece.x/62.5 == 0:
            return True

# Checks if a move would cause an enemy jump
def doesMoveEscape(board, move, color):
    enemy_jumps = findJumps(board, not color)
    for jump in enemy_jumps:
        for victim in jump.jumped:
            if victim.x/62.5 == move.checker.x and victim.y/62.5 == move.checker.y:
                return True
    return False

# Does the work of computing what move to do next
def minimax(depth, color, board, h=2):
    if color:
        black_moves = weighBoard(board)[1]
    elif not color:
        white_moves = weighBoard(board)[0]
    if depth == h:
        if color:
            # Min
            # Returns move best for black
            min = None
            for move in black_moves:
                if min == None:
                    min = move
                elif min.weight > move.weight:
                    min = move
            return min
        else:
            # Max
            # Returns move best for white
            max = None
            for move in white_moves:
                if max == None:
                    max = move
                elif max.weight < move.weight:
                    max = move
            return max

    best_move = None
    if color:
        # Min
        for move in black_moves:
            if move.type == "Jump":
                # The Ai has to jump
                return move

        # Evaluates future impact of moves and ranks them accordingly
        for move in black_moves:
            copy = model.copyBoard(board)
            val = minimax(depth + 1, False, move.apply(copy))
            if best_move == None or val.weight < best_move.weight:
                best_move = val

    else:
        # Evaluates future impact of moves and ranks them accordingly
        for move in white_moves:
            val = minimax(depth + 1, True, move.apply(model.copyBoard(board)))
            if best_move == None or val.weight > best_move.weight:
                best_move = val
    return best_move