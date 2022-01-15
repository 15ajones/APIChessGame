""" 
this file is responsible for handling user input and displaying the current game state object

"""
import ChessEngine
import pygame as p
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
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
    gs = ChessEngine.GameState()
    load_images()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen,gs):#responsible for all chess graphics
    drawBoard(screen) 
    drawPieces(screen,gs.board) 

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





    
     

