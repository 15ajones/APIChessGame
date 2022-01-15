"""

stores all info about the current state of the chess game
also responsible for determining if a move is valid or not
also keeps a move log

"""

class Game:
    def __init__(self, user_is_white):
        import chess
        import chess.engine
        self.robot_white=False if user_is_white else True
        self.turn_white=True
        self.game_over=False
        self.engine=chess.engine.SimpleEngine.popen_uci('/usr/local/Cellar/stockfish/14.1/bin/stockfish') #starts stockfish engine
        self.board=chess.Board() #creates board
        self.move = "" #string storing most recent move
        self.moves=[] #list of strings showing all moves in order
        self.board_indexer={#used to produce piece_moved_to
            "a":0,
            "b":2,
            "c":4,
            "d":6,
            "e":8,
            "f":10,
            "g":12,
            "h":14,
            "1":112,
            "2":96,
            "3":80,
            "4":64,
            "5":48,
            "6":32,
            "7":16,
            "8":0
        }

