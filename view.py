import graphics
from graphics import Point
import model
from time import sleep
import ai
import time


width = 500
height = 500
offset_x = width / 8
offset_y = height / 8
win = graphics.GraphWin("Checkers", width, height)


def drawBoard():
    color_offset = False
    for x in range(0, 8):
        if x % 2 == 1:
            color_offset = True
        else:
            color_offset = False
        for y in range(0, 8):
            point = Point(x * offset_x, y * offset_y)
            box = graphics.Rectangle(point, Point(point.x + offset_x, point.y + offset_y))
            box.setFill("Gray")
            if color_offset:
                if x % 2 == 0 or y % 2 == 0:
                    box.setFill("#c2ab56")
            elif x % 2 == 1 or y % 2 == 1:
                box.setFill("#c2ab56")
            box.draw(win)


def drawCheckers():
    for piece in model.board.flat:
        if piece.checker is not None:
            circle = graphics.Circle(Point(piece.center[0], piece.center[1]), 15)
            if piece.checker.black:
                circle.setFill("Black")
            else:
                circle.setFill("White")
            circle.draw(win)


def findPiece(click):
    click_x = click.x/62.5
    click_y = click.y/62.5
    for x in range(0, 8):
        for y in range(0, 8):
            if (click_x > x and click_y > y) and (click_x < x+1 and click_y < y+1):
                return (x, y)
    return None





def redraw():
    for child in win.children:
        child.undraw()
    drawBoard()
    drawCheckers()


def runAI(color):
    t1 = time.time()
    ai_move = ai.minimax(0, color, model.board, float("-inf"), float("inf"))
    t2 = time.time()
    print(t2-t1)
    ai_move.apply(model.board)
    redraw()
    return ai_move


def chooseDif():
    difwin = graphics.GraphWin("Choose Difficulty")
    difwin.focus()
    entry = graphics.Entry(Point(100, 100), 20)
    entry.setText("2")
    entry.draw(difwin)
    difwin.getMouse()
    ai.DIFFICULTY = int(entry.getText())
    difwin.close()

def playerTurn(color):
    while True:
        click1 = win.getMouse()
        checker = findPiece(click1)
        if checker is None or model.board[int(checker[0]), int(checker[1])].checker is None or model.board[int(checker[0]), int(checker[1])].checker.black is not color:
            continue
        click2 = win.getMouse()
        piece = findPiece(click2)
        if piece is None or (piece[0] == checker[0] and piece[1] == checker[1]):
            continue
        partial_move = ai.Move(model.board[int(checker[0]), int(checker[1])].checker, model.board[int(piece[0]), int(piece[1])],"?")
        partial_move.checker.x = checker[0]
        partial_move.checker.y = checker[1]
        move = model.getFullMove(partial_move)
        if move is None:
            continue
        else:
            move.apply(model.board)
            return

def draw():
    chooseDif()
    drawBoard()
    drawCheckers()
    while model.hasWon(model.board) == 0:
        sleep(0.01)
        model.King(model.board)
        playerTurn(False)
        model.King(model.board)
        redraw()
        win.update()
        runAI(True)
    winWindow = graphics.GraphWin("Game over")
    if model.hasWon(model.board) == 1:
        text = graphics.Text(Point(winWindow.width/2, winWindow.height/2), "You Won!!")
        text.draw(winWindow)
        sleep(3)
    elif model.hasWon(model.board) == -1:
        text = graphics.Text(Point(winWindow.width / 2, winWindow.height / 2), "You Lost :(")
        text.draw(winWindow)
        sleep(3)
    return




