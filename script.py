import view
import ai
import model
model.checkers[4].king = True
model.checkers[4].piece.checker = model.checkers[4]
model.checkers[6].black = False
model.checkers[6].piece.checker = model.checkers[6]
model.checkers[9].piece.checker = None
model.checkers[9] = None
def minimaxTest():
    scores = ai.findValues(model.checkers[4])
    res = ai.minimax(0,0,scores[2],True,scores[0],3)
    print(res)

minimaxTest()

actions = ai.findActions(model.checkers[4])
view.draw()



