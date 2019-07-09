## Used for copying a matrix so the AI can calculate into the future 
from copy import copy, deepcopy
import random
import math

## Prints the board
def print_board(board):
    for i in range(7):
        print(board[i])
        print ("")

## Returns a list of valid moves 
def valid_move(board):
    valid = []
    for i in range(7):
        if (board[0][i] == '_'):
            valid.append(i)
    return valid

## Makes a move
def make_move(board, piece, pos):
    for i in range(5,-1,-1):
        if (board[i][pos] == '_'):
            board[i][pos] = piece
            break

## Checks if any player has won
def win(board):
    ##horizontal
    for h in range(6):
        for i in range(4):
            if (board[h][i] == "X" and board[h][i+1] == "X" and board[h][i+2] == "X" and board[h][i+3] == "X"):
                return 1
            elif (board[h][i] == "O" and board[h][i+1] == "O" and board[h][i+2] == "O" and board[h][i+3] == "O"):
                return 2
    ##vertical
    for i in range(7):
        for h in range(3):
            if (board[h][i] == "X" and board[h+1][i] == "X" and board[h+2][i] == "X" and board[h+3][i] == "X"):
                return 1
            elif (board[h][i] == "O" and board[h+1][i] == "O" and board[h+2][i] == "O" and board[h+3][i] == "O"):
                return 2
    #positive diagonal
    for i in range(4):
        for h in range(3,6):
            if (board[h][i] == "X" and board[h-1][i+1] == "X" and board[h-2][i+2] == "X" and board[h-3][i+3] == "X"):
                return 1
            elif (board[h][i] == "O" and board[h-1][i+1] == "O" and board[h-2][i+2] == "O" and board[h-3][i+3] == "O"):
                return 2
    #negative diagonal
    for h in range(3):
        for i in range(4):
            if (board[h][i] == "X" and board[h+1][i+1] == "X" and board[h+2][i+2] == "X" and board[h+3][i+3] == "X"):
                return 1
            elif (board[h][i] == "O" and board[h+1][i+1] == "O" and board[h+2][i+2] == "O" and board[h+3][i+3] == "O"):
                return 2

## Evaluates based on pieces in windows of 4
def evaluate(good, blank, bad, sc):
    if (good == 2 and blank == 2):
        sc += 2
        # + 2 
    elif (good == 3 and blank == 1):
        sc += 5
        # + 5
    elif (good == 4):
        sc += 100
    if (bad == 3 and blank == 1):
        sc -= 4
        # - 4
    if (bad == 2 and blank == 2):
        sc -= 3
        # - 3
    return sc

## Determines the value of the given board
def score(board, piece, enemy):
    sc = 0
    ## Center preference
    for i in range(6):
        center = [l[3] for l in board]
    good = center.count(piece)
    sc += good * 6
    
    ## Horizontal
    for i in range(6):
        row = board[i]
        for l in range(4):
            small_row = row[l:l+4]
            #print(small_row)
            good = small_row.count(piece)
            blank = small_row.count('_')
            bad = small_row.count(enemy)
            #print("A",good)
            #print("B",blank)
            sc = evaluate(good, blank, bad, sc)

    ## Vertical
    for i in range(7):
        column = [l[i] for l in board]
        #print(column)
        for h in range(3):
            small_col = column[h:h+4]
            good = small_col.count(piece)
            blank = small_col.count('_')
            bad = small_row.count(enemy)
            #print("A",good)
            #print("B",blank)
            sc = evaluate(good, blank, bad, sc)
            
    ## Positive Slope
    for i in range(5,2,-1):
        for l in range (4):
            slope = [board[i-r][l+r] for r in range(4)]
            good = slope.count(piece)
            blank = slope.count('_')
            bad = small_row.count(enemy)
            #print(slope)
            #print("A",good)
            #print("B",blank)
            sc = evaluate(good, blank, bad, sc)
            
    ## Negative Slope
    for i in range(3):
        #print("")
        for l in range (4):
            slope = [board[i+r][l+r] for r in range(4)]
            good = slope.count(piece)
            blank = slope.count('_')
            bad = small_row.count(enemy)
            #print(slope)
            #print("A",good)
            #print("B",blank)
            sc = evaluate(good, blank, bad, sc)
            
    return sc

def minimax(board, depth, maxplayer, piece, enemy):
    valid = valid_move(board)
    if depth == 0 or len(valid) == 0 or win(board) == 2 or win(board) == 1:
        if len(valid) == 0:
            return (None, 0)
        if win(board) == 2:
            #print("AA")
            return (None, 100000000000)
        if win(board) == 1:
            return (None, -100000000000)
        if depth == 0:
            return (None, score(board, piece, enemy))
    if maxplayer:
        value = -1000000000000000000
        col = random.choice(valid)
        for c in valid:
            board_copy = deepcopy(board)
            make_move(board_copy, piece, c)
            garb, new_score = minimax(board_copy, depth - 1, False, enemy, piece)
            if (new_score > value):
                #print("A", new_score, c)
                value = new_score
                col = c
        return col, value
    else:
        value = 10000000000000000000
        col = random.choice(valid)
        for c in valid:
            board_copy = deepcopy(board)
            make_move(board_copy, enemy, c)
            garb, new_score = minimax(board_copy, depth - 1, True, piece, enemy)
            if (new_score < value):
                #print("B", new_score, c)
                value = new_score
                col = c
        return col, value

def pick_best(board, piece, enemy):
    valid = valid_move(board)
    best_sc = -100000000
    best_col = random.choice(valid)
    for col in valid:
        #print("col", col)
        #print("valid", valid)
        temp_board = deepcopy(board)
        make_move(temp_board, piece, col)
        sc = score(temp_board, piece, enemy)
        #print("score", sc)
        if (sc > best_sc):
            #print("collllll", col)
            best_sc = sc
            best_col = col
        #print ("")
    return best_col



play = "y"

while (play == "y" or play == "Y"):

    ## Default board
    Board = [['_','_','_','_','_','_','_'],
             ['_','_','_','_','_','_','_'],
             ['_','_','_','_','_','_','_'],
             ['_','_','_','_','_','_','_'],
             ['_','_','_','_','_','_','_'],
             ['_','_','_','_','_','_','_'],
             ['1','2','3','4','5','6','7']]

    Gamestate = 1
    Player = 1
    AI = 2
    Player_Piece = "X"
    AI_Piece = "O"
    vic = 0

    who_move = random.randint(1,2)

    print_board(Board)


    while (Gamestate):
        valid = valid_move(Board)
        ## Player move
        if (who_move == 1):
            check = 0
            while (check == 0):


    ##########            ##2 AI NOT RECOMMENDED
    ########            move, minimax_score = minimax(Board, 4, True, Player_Piece, AI_Piece)
    ##########            #move = int(input("Player 2. Enter which Column you would like to put your piece: "))
    ##########            move = pick_best(Board, Player_Piece, AI_Piece)
    ########            print("my pick", move + 1)
    ########            #print("move",move)
    ########            #print(valid)
    ########            if move in valid:
    ########                check = 1
    ########                make_move(Board, Player_Piece, move)
    ########                who_move = 0
    ########                #print(score(Board, AI_Piece))
    ########                vic = win(Board)
    ########                break
    ########            else:
    ########                print("Enter a valid move")
    ########                check = 1

                
    ##            ## HUMAN
                move = int(input("Player 1. Enter which Column you would like to put your piece: "))
                move -= 1
                #print("move",move)
                #print(valid)
                if move in valid:
                    check = 1
                    make_move(Board, Player_Piece, move)
                    who_move = 0
                    #print(score(Board, Player_Piece))
                    vic = win(Board)
                    break
                else:
                    print("Enter a valid move")
            

        ## AI move
        else:
            check = 0
            while (check == 0):
    ##            move = int(input("Player 2. Enter which Column you would like to put your piece: "))
    ##            move -= 1
    ##            move = pick_best(Board, AI_Piece, Player_Piece)
                move, minimax_score = minimax(Board, 4, True, AI_Piece, Player_Piece)
                #print(minimax_score)
                print("AI pick", move + 1)
                #print("move",move)
                #print(valid)
                if move in valid:
                    check = 1
                    make_move(Board, AI_Piece, move)
                    #score(Board, AI_Piece, Player_Piece)
                    who_move = 1
                    #print(score(Board, AI_Piece))
                    vic = win(Board)
                    break
                else:
                    print("Enter a valid move")
                    check = 1

        print_board(Board)

        if vic == 1:
           print("Player 1 wins")
           play = input("Play again? (y/n)")
           break;
        elif vic == 2:
           print("Player 2 wins")
           play = input("Play again? (y/n)")
           break;
    






