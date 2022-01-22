from ChessEngine import Game
import chess
import chess.engine

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
    p.init()
    
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game = Game(True)
    load_images()
    running = True
    move_array=[]
    move = ""
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif game.turn_white!=game.robot_white:
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
                                game.board.push(chess.Move.from_uci(move))
                                game.turn_white = not game.turn_white
                            move_array=[]
            else:
                move=game.engine.play(game.board, chess.engine.Limit(time=0.1)).move
                print(move)
                game.board.push(move)
                game.turn_white = not game.turn_white  
        pygame_board = translate_board(game) #need to change so its different if youre black or if youre white
        drawGameState(screen,pygame_board)
        clock.tick(MAX_FPS)
        p.display.flip()

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

        


def drawGameState(screen,board):#responsible for all chess graphics
    drawBoard(screen) 
    drawPieces(screen,board) 

def drawBoard(screen):#this function draws squares on the board
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



    
     