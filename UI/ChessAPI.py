import berserk
from ChessEngine import Game
import chess
import chess.engine
import time

import pygame as p
WIDTH = HEIGHT = 512 # of chess board
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
ROW_INDEXER = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h" 
}

#gunna initialise a global dictionary of images once (only once cos its a costly process)

def load_images():
    IMAGES["P"]=p.transform.scale(p.image.load("images/wp.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["B"]=p.transform.scale(p.image.load("images/wB.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["K"]=p.transform.scale(p.image.load("images/wK.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["Q"]=p.transform.scale(p.image.load("images/wQ.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["N"]=p.transform.scale(p.image.load("images/wN.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["R"]=p.transform.scale(p.image.load("images/wR.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["p"]=p.transform.scale(p.image.load("images/bp.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["b"]=p.transform.scale(p.image.load("images/bB.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["q"]=p.transform.scale(p.image.load("images/bQ.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["k"]=p.transform.scale(p.image.load("images/bK.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["n"]=p.transform.scale(p.image.load("images/bN.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES["r"]=p.transform.scale(p.image.load("images/bR.png"), (SQ_SIZE, SQ_SIZE))

#this next bit handles uder input and updating of graphics

def main():
    session = berserk.TokenSession("lip_91oyBEwFziL22bkIG82c")
    client = berserk.Client(session)
    board = berserk.clients.Board(session)
    account_data = client.account.get()
    player_id = account_data["id"]
 
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
                stream = board.stream_game_state(event['game']['id'])
                break
            else:
                print("You're playing as white!")
                stream = board.stream_game_state(event['game']['id'])
                break
    game_id=event['game']['id']
    game = Game(isWhite)   
    p.init()
    screen = p.display.set_mode((WIDTH+300, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    load_images()
    running = True
    move_array=[]
    game_over=False
    move = ""
    row = column = half_move = 0
    white_time = black_time = 0.0
    old_white_time = white_time
    old_black_time = black_time
    t0 = time.time()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # elif game.turn_white!=game.robot_white: #uncomment for stockfish black
            elif game.turn_white == isWhite:
                white_time = old_white_time + time.time()-t0   #comment for stockfish black
                if e.type == p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos() #gets location of mouse click
                    row = location[0]//SQ_SIZE
                    column = location[1]//SQ_SIZE
                    half_move=ROW_INDEXER[row]+str(8-column)
                    if len(move_array)==0:
                        move_array.append(half_move)
                        print("1")
                        
                    elif len(move_array)==1:
                        if half_move == move_array[0]:
                            move_array=[] #cancels move
                        else:
                            move_array.append(half_move)
                            print("2")
                            move=str(move_array[0])+str(move_array[1])
                            if chess.Move.from_uci(move) in game.board.legal_moves:
                                board.make_move(game_id, game.board.parse_san(move))
                                game.board.push(chess.Move.from_uci(move))
                                old_white_time = white_time
                                game.turn_white = not game.turn_white
                                t0=time.time()
                                move_array=[]
                            else:
                                move_array=[]
                                move_array.append(half_move)
                


                            
            else: #uncomment for stockfish black
                for event in stream:
                    black_time = old_black_time + time.time()-t0
                    drawTimer(screen, white_time, black_time)
                    print("here")
                    if event['type']=='gameState':
                        print(event)
                        if event['status']=='aborted':
                            game_over=True
                            break
                        try:
                            print(str(event["moves"].split()[-1]))
                            game.board.push_uci(event["moves"].split()[-1])
                            old_black_time = black_time
                            t0 = time.time()
                            break
                        except:
                            pass
                game.turn_white = not game.turn_white

        
        pygame_board = translate_board(game) #need to change so its different if youre black or if youre white
        drawGameState(screen,pygame_board)
        highlightSquares(screen, game,pygame_board,half_move,row,column,move_array)
        drawTimer(screen, white_time, black_time)
        if game.board.is_checkmate():
            game_over=True
            if game.turn_white:
                drawText(screen, "Black wins by checkmate!")
            else:
                drawText(screen, "White wins by checkmate!")
        elif game.board.is_game_over():
            game_over=True
            drawText(screen, "Draw!")
        elif game_over:
            drawText(screen, "TIMEOUT")
        clock.tick(MAX_FPS)
        p.display.flip()

def drawTimer(screen, white_time, black_time):
    global colors
    color = colors[1]
    p.draw.rect(screen,color,p.Rect(8*DIMENSION+448, 0, 300, HEIGHT/2))
    font = p.font.SysFont('arial', 80, True, False)
    color = colors[0]
    p.draw.rect(screen, color, p.Rect(8*DIMENSION+448, HEIGHT/2, 300, HEIGHT/2))
    black_countdown = 600-int(black_time)
    black_time_text = str(black_countdown//60)+":"+str(black_countdown%60) if len(str(black_countdown%60))>1 else str(black_countdown//60)+":"+"0"+str(black_countdown%60)
    textObject = font.render(black_time_text if black_countdown > 0 else "0", 0, p.Color("Black"))
    textLocation = p.Rect(8*DIMENSION+448, 0, 300, HEIGHT/2).move(WIDTH/3 - textObject.get_width()/2, HEIGHT/4 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    white_countdown = 600-int(white_time)
    white_time_text = str(white_countdown//60)+":"+str(white_countdown%60) if len(str(white_countdown%60))>1 else str(white_countdown//60)+":"+"0"+str(white_countdown%60)
    textObject = font.render(white_time_text if white_countdown > 0 else "0", 0, p.Color("Black"))
    textLocation = p.Rect(8*DIMENSION+448, HEIGHT/2, 300, HEIGHT/2).move(WIDTH/3 - textObject.get_width()/2, HEIGHT/4 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    
def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0,0,WIDTH, HEIGHT).move(WIDTH/2 -textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

def translate_board(game):
    pygame_board = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        []
    ]
    row = 0
    for i in range(len(str(game.board))):
        if str(game.board)[i]=="\n":
            row+=1
        elif str(game.board)[i]!=" ":
            pygame_board[row].append(str(game.board)[i])
    return pygame_board

def highlightSquares(screen, game,pygame_board,half_move=None, row=None, column=None,move_array=None):#highlights piece currently selected
    if (half_move == None) or (half_move == 0):
        return
    if len(move_array)!=1:
        return

    piece = pygame_board[column][row]
    if piece ==".":
        return    
    if (game.turn_white and piece.isupper()) or (not game.turn_white and piece.islower()):
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color('blue'))
        screen.blit(s, (row*SQ_SIZE, column*SQ_SIZE))



    
def drawGameState(screen,board):#responsible for all chess graphics
    drawBoard(screen) 
    drawPieces(screen,board) 

def drawBoard(screen):#this function draws squares on the board
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    white = False
    for i in range(DIMENSION):
        white = not white
        for j in range(DIMENSION):
            if white:
                color = colors[0]
            else:
                color = colors[1]
            p.draw.rect(screen,color,p.Rect(i*SQ_SIZE, j*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            white = not white

def drawPieces(screen,board):#this function draws pieces on top of those squares
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != ".":
                screen.blit(IMAGES[piece], p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))



if __name__ == "__main__":
    main()


