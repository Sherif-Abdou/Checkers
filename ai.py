import model
import math

class Move():
    def __init__(self,checker, piece, type):
        self.checker = checker
        self.piece = piece
        self.type = type

def checkNeighbor(x,y,px,py,up=False,down=False,dir=-1):
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


def checkDirection(x, y, dir):
    if x < 0 or y<0 or x > 7 or y > 7 or dir[0] == -1:
        return
    if dir[0] == 0:
        new_x = x+1
        new_y = y+1
    if dir[0] == 1:
        new_x = x-1
        new_y = y+1
    if dir[0] == 2:
        new_x = x+1
        new_y = y-1
    if dir[0] == 3:
        new_x=x-1
        new_y=y-1
    new_piece = model.board[int(new_x), int(new_y)]
    if new_piece.checker != None:
        checkDirection(new_x, new_y, dir)
    return new_piece

def findActions(checker):
    piece = checker.piece
    px = piece.x/62.5
    py = piece.y/62.5
    results = []
    for i in model.board.flat:
        x = i.x/62.5
        y = i.y/62.5
        if i.checker == None:
            if checker.black or checker.king:
                dir = checkNeighbor(x,y,px,py,down=True)
                if dir[0] != -1:
                    move = Move(checker,i, "Move")
                    results.append(move)
            if checker.black == False or checker.king:
                dir = checkNeighbor(x,y,px,py,up=True)
                if dir[0] != -1:
                    move = Move(checker, i, "Move")
                    results.append(move)
        else:
            if (checker.black and i.checker.black == False) or checker.king:
                """Checks if piece in the same direction of the opposing checker is empty"""
                nei = checkNeighbor(x,y,px,py)
                test = []
                for di in nei:
                    if di == 0:
                        if model.board[int(px+1),int(py+1)].checker == None:
                            nei.remove(di)
                    if di == 1:
                        if model.board[int(px-1),int(py+1)].checker == None:
                            nei.remove(di)
                    if di == 2:
                        if model.board[int(px+1),int(py-1)].checker == None:
                            nei.remove(di)
                    if di == 3:
                        if model.board[int(px-1)][int(py-1)].checker is None:
                            nei.remove(di)
                re = checkDirection(px, py, nei)
                if re != None:
                    move = Move(checker, re, "Jump")
                    results.append(move)

            if (checker.black == False and i.checker.black == True) or checker.king:
                pass
    return results


def doesKing(checker, param):
    if checker.black:
        if checker.piece.y/62.5 == 7:
            return True
    if checker.black == False:
        if checker.piece.y/62.5 == 0:
            return True

    return False


def doesProtect(checker, param):
    return False


def findValues(checker):
    actions = findActions(checker)
    res = [[],[]]
    x = 0
    for action in actions:
        if action.type == "Move":
            res[0].append(3)
        if action.type == "Jump":
            res[0].append(5)

        if doesKing(checker, action.piece):
            res[0].append(7)

        if doesProtect(checker, action.piece):
            res[0].append(9)

        res[1].append(action)
        x += 1
    res.append(x)
    return res
def log2(n):
    if n == 1:
        return 0
    else:
        return 1+log2(n/2)


def minimax(depth, nodeIndex, possible, isMax, pieces, h):
    if depth == h or depth == 3:
        return pieces[nodeIndex]

    if isMax:
        return max(minimax(depth+1,nodeIndex*possible[depth],possible,False,pieces,h),
                   minimax(depth+1,nodeIndex*possible[depth]+possible[depth]/2,possible,False,pieces,h))
    else:
        return min(minimax(depth + 1, nodeIndex * possible[depth],possible, True, pieces, h),
                   minimax(depth + 1, nodeIndex * possible[depth] + possible[depth] / 2,possible, True, pieces, h))


