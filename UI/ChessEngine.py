"""

stores all info about the current state of the chess game
also responsible for determining if a move is valid or not
also keeps a move log

"""

class GameState():
    def __init__(self):
        board = [ #represented by a 8x8 list
            ["r","n","b","q","k","b","n","r"],
            ["p","p","p","p","p","p","p","p"],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            [".",".",".",".",".",".",".","."],
            ["P","P","P","P","P","P","P","P"],
            ["R","N","B","Q","K","B","N","R"]
        ]
        whiteToMove = True
        moveLog=[]