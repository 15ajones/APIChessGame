import threading
import datetime
import chess
import os

chess_board = chess.Board()
runOnce = True

class Game(threading.Thread):
    def __init__(self, board, game_id, player_id, player_white, color, time, **kwargs):
        super().__init__(**kwargs)
        super().__init__(**kwargs)
        self.game_id = game_id
        self.board = board
        self.stream = board.stream_game_state(game_id)
        self.player_id = player_id
        self.isWhite = isWhite
        self.color = color
        self.clock = {'white': datetime.datetime(1970, 1, 1, 0, time, 0), 'black': datetime.datetime(1970, 1, 1, 0, time, 0)}
        self.first_move = 2 # returns false after 2 moves have been made
        if self.isWhite:
            self.white_first_move()
    
    def run(self):
        def run(self):
            for event in self.stream:
                if event['type'] == "gameFull":
                    self.handle_game_full(event)
                elif event['type'] == 'gameState':
                    self.handle_state_change(event)
                elif event['type'] == 'chatLine':
                    self.handle_chat_line(event)
    
