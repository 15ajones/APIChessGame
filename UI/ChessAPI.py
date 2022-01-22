import berserk
client = berserk.Client()
session = berserk.TokenSession(lip_91oyBEwFziL22bkIG82c)
client = berserk.Client(session)
board = berserk.clients.Board(session)
account_data = client.account.get()
player_id = account_data["id"]

class Game():
    def __init__(self, client, game_id, **kwargs):
        super().__init__(**kwargs)
        self.game_id = game_id
        self.client = client
        self.stream = client.bots.stream_game_state(game_id)
        self.current_state = next(self.stream)
    def run(self):
        for event in self.stream:
            if event['type'] == 'gameState':
                self.handle_state_change(event)
            elif event['type'] == 'chatLine':
                self.handle_chat_line(event)
    def handle_state_change(self, game_state):
        print(game_state)
    def handle_chat_line(self, chat_line):
        print(chat_line)
 
print("Searching after opponent...")
board.seek(10, 0)
for event in board.stream_incoming_events():
        if event['type'] == 'gameStart':
            print("An opponent was found!")

            isWhite = True
            color = "Black" # We set the color to the opposite color of the player

            if player_id != client.games.export(event['game']['id'])['players']['white']['user']['id']:
                isWhite = False
                color = "White"
                print("You're playing as black!")
                print("White's turn...")
            else:
                print("You're playing as white!")