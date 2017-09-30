import ai
import model
import math
from copy import deepcopy
def takeChecker(x,y, board):
    board[x,y].checker = None
def testBoard1():
    testboard1 = deepcopy(model.board)
    takeChecker(0,1,testboard1)
    takeChecker(5,2,testboard1)
    takeChecker(1,6, testboard1)
    results1 = ai.findMoves(testboard1, True)
    results2 = ai.findMoves(testboard1, False)

    if len(results1) == 8 and len(results2) == 9:
        if results1[0].piece.x/62.5 == 0 and results1[0].piece.y/62.5 == 1:
            print("Test1: True")
    else:
        print("Test1: False")

def testBoard2():
    testboard1 = deepcopy(model.board)
    takeChecker(3, 5, testboard1)
    takeChecker(1, 0, testboard1)
    takeChecker(7, 6, testboard1)
    results1 = ai.findMoves(testboard1, True)
    results2 = ai.findMoves(testboard1, False)
    actual = [(1,4),(1,4),(3,4),(3,4),(5,4),(5,4),(7,4),(7,6)]
    if len(results1) == 7 and len(results2) == 8:
        x = 0
        true = True
        for move in results2:
            if move.piece.x/62.5 == actual[x][0] and move.piece.y/62.5 == actual[x][1]:
                pass
            else:
                true == False
            x+=1
        if true:
            print("Test2: True")
    else:
        print("Test2: False")

testBoard1()
testBoard2()

