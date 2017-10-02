import ai
import model
import math
import uuid
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

# testBoard1()
# testBoard2()
def testjump3():
    testboard3 = deepcopy(model.board)
    testboard3[1,2].checker.black = False
    jumps = ai.findJumps(testboard3, True)
    actual = [(2,3),(0,3)]
    x = 0
    fail = False
    for jump in jumps:
        if jump.piece.x/62.5 == actual[x][0] and jump.piece.y/62.5 == actual[x][1]:
            pass
        else:
            fail = True

        x+=1

    if fail == False:
        print("Test3: Works")

    val = ai.minimax(0, True, testboard3)
    print(val)

def testjump4():
    testboard4 = deepcopy(model.board)
    testboard4[1, 2].checker.black = False
    checker = testboard4[0,5].checker
    testboard4[0,5].checker = None
    testboard4[1,4].checker = checker
    checker.piece = testboard4[1, 4]
    val = ai.minimax(0, True, testboard4)
    jumps = ai.findJumps(testboard4, True)
    actual = [(2,3),(0,3)]

testjump4()
testjump3()

def testapplymove():
    testboard = deepcopy(model.board)
    results = ai.findMoves(testboard, True)
    board = results[0].apply(testboard)
    print(board)

# testapplymove()
#
# val = ai.minimax(0,False, model.board)
# print(val)