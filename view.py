import graphics
from graphics import Point
import model
from time import sleep
width = 500
height = 500
offset_x = width/8
offset_y = height/8
win = graphics.GraphWin("Checkers", width, height)




def drawBoard():
    color_offset = False
    for x in range(0,8):
        if x%2 == 1:
            color_offset = True
        else:
            color_offset = False
        for y in range(0,8):
            point = Point(x*offset_x,y*offset_y)
            box = graphics.Rectangle(point, Point(point.x+offset_x, point.y+offset_y))
            box.setFill("Gray")
            if color_offset:
                if x%2 == 0 or y%2 == 0:
                    box.setFill("#c2ab56")
            elif x%2 == 1 or y%2 == 1:
                    box.setFill("#c2ab56")
            box.draw(win)

def drawCheckers():
    board = model.board
    for piece in board.flat:
        if piece.checker != None:
            circle = graphics.Circle(Point(piece.center[0],piece.center[1]), 15)
            print(piece.center[0],piece.center[1])
            if piece.checker.black == True:
                circle.setFill("Black")
            else:
                circle.setFill("White")
            piece.checker.circle = circle
            circle.draw(win)


def checkMove():
    if win.getMouse() != None:
        for checker in model.checkers:
            pass



def draw():
    drawBoard()
    drawCheckers()
    #sleep(4)
    #model.checkers[0].moveChecker(model.board[0,0])
    while True:
        checkMove()