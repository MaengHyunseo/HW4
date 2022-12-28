import pygame
import os
import numpy as np

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 750
WHITE = (255, 255, 255)

pygame.init()
pygame.display.set_caption("TIC TAC TOE")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# load images
current_path = os.path.dirname(__file__)
img_path = os.path.join(current_path, 'img')
BOARD = pygame.image.load(os.path.join(img_path, "board.jpg"))
Ximg = pygame.image.load(os.path.join(img_path, "X.png"))
Oimg = pygame.image.load(os.path.join(img_path, "O.png"))
alphaImg = pygame.image.load(os.path.join(img_path, "alpha.png"))

# fonts
font = pygame.font.SysFont('applesdgothicneo', 35)

def setPlayerMark():
    # Randomly assign player's mark between X or O
    if np.random.randint(0,2) == 0:
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if np.random.randint(0,2) == 0:
        return 'You'
    else:
        return 'computer'

def makeMove(board, mark, move, markImg):
    board[move] = mark
    
    # display the mark image
    if move == 7:
        screen.blit(markImg, (0, 0))
    elif move == 8:
        screen.blit(markImg, (200, 0))
    elif move == 9:
        screen.blit(markImg, (400, 0)) 
    elif move == 4:
        screen.blit(markImg, (0, 200))
    elif move == 5:
        screen.blit(markImg, (200, 200)) 
    elif move == 6:
        screen.blit(markImg, (400, 200))
    elif move == 1:
        screen.blit(markImg, (0, 400))
    elif move == 2:
        screen.blit(markImg, (200, 400))
    elif move == 3:
       screen.blit(markImg, (400, 400))
    pygame.display.update()

def isWinner(board, mark):
    return ((board[7] == mark and board[8] == mark and board[9] == mark) or 
    (board[4] == mark and board[5] == mark and board[6] == mark) or 
    (board[1] == mark and board[2] == mark and board[3] == mark) or 
    (board[7] == mark and board[4] == mark and board[1] == mark) or 
    (board[8] == mark and board[5] == mark and board[2] == mark) or 
    (board[9] == mark and board[6] == mark and board[3] == mark) or 
    (board[7] == mark and board[5] == mark and board[3] == mark) or 
    (board[9] == mark and board[5] == mark and board[1] == mark))

def getBoardCopy(board):
    # Make a copy of the board list and return it.
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy

def isSpaceFree(board, move):
    # Return true if the passed move is free on the passed board.
    return board[move] == ' '

def getPlayerMove(board):
    move = ' '
    
    while True:
        m_x, m_y = pygame.mouse.get_pos()
        if m_x < 200 and m_y < 200:
            move = 7
        elif m_x < 400 and m_y < 200:
            move = 8
        elif m_x < WINDOW_WIDTH and m_y < 200:
            move = 9
        elif m_x < 200 and m_y < 400:
            move = 4
        elif m_x < 400 and m_y < 400:
            move = 5
        elif m_x < WINDOW_WIDTH and m_y < 400:
            move = 6
        elif m_x < 200 and m_y < WINDOW_HEIGHT:
            move = 1
        elif m_x < 400 and m_y < WINDOW_HEIGHT:
            move = 2
        else:
            move = 3
        
        if isSpaceFree(board, move):
            break

    return move

def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return np.random.choice(possibleMoves)
    else:
        return None

def getComputerMove(board, cprMark):
    if cprMark == 'X':
        plrMark = 'O'
    else:
        plrMark = 'X'

    # Here is our algorithm for our Tic Tac Toe AI:
    # First, check if we can win in the next move
    for i in range(1, 10):
        BoardCopy = getBoardCopy(board)
        if isSpaceFree(BoardCopy, i):
            makeMove(BoardCopy, cprMark, i, alphaImg)
            if isWinner(BoardCopy, cprMark):
                return i

    # Check if the player could win on his next move, and block them.
    for i in range(1, 10):
        BoardCopy = getBoardCopy(board)
        if isSpaceFree(BoardCopy, i):
            makeMove(BoardCopy, plrMark, i, alphaImg)
            if isWinner(BoardCopy, plrMark):
                return i

    # Try to take one of the corners, if they are free.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # Try to take the center, if it is free.
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

def main():
    screen.blit(BOARD, BOARD.get_rect())

    board = [' '] * 10

    plrMark, cprMark = setPlayerMark()
    if plrMark == 'X':
        plrImg = Ximg
        cprImg = Oimg
    else:
        plrImg = Oimg
        cprImg = Ximg

    turn = whoGoesFirst()

    message = font.render("You are " + plrMark + "!  " +  turn + " goes first.", True, WHITE)
    center = int(WINDOW_WIDTH / 2) - int(message.get_width() / 2)
    screen.blit(message, (center, WINDOW_HEIGHT - 100))

    pygame.display.update()

    gameIsPlaying = True
    while gameIsPlaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameIsPlaying = False
            # Player's turn
            if turn == 'You':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    move = getPlayerMove(board)
                    makeMove(board, plrMark, move, plrImg)

                    if isWinner(board, plrMark):
                        win = font.render("You have won the game!", True, WHITE)
                        center = int(WINDOW_WIDTH / 2) - int(win.get_width() / 2)
                        screen.blit(win, (center, WINDOW_HEIGHT - 50))
                        pygame.display.update()
                        gameIsPlaying = False
                    else:
                        if isBoardFull(board):
                            tie = font.render("The game is a tie!", True, WHITE)
                            center = int(WINDOW_WIDTH / 2) - int(tie.get_width() / 2)
                            screen.blit(tie, (center, WINDOW_HEIGHT - 50))
                            pygame.display.update()
                            break
                        else:
                            turn = 'computer'

            # Computer's turn                
            else:
                move = getComputerMove(board, cprMark)
                makeMove(board, cprMark, move, cprImg)

                if isWinner(board, cprMark):
                    lose = font.render("The computer has beaten you! You lost.", True, WHITE)
                    center = int(WINDOW_WIDTH / 2) - int(lose.get_width() / 2)
                    screen.blit(lose, (center, WINDOW_HEIGHT - 50))
                    pygame.display.update()
                    gameIsPlaying = False
                else:
                    if isBoardFull(board):
                        tie = font.render("The game is a tie!", True, WHITE)
                        center = int(WINDOW_WIDTH / 2) - int(tie.get_width() / 2)
                        screen.blit(tie, (center, WINDOW_HEIGHT - 50))
                        pygame.display.update()
                        gameIsPlaying = False
                    else:
                        turn = 'You'

    pygame.display.flip()
    clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.time.delay(10000)
    pygame.quit()