import piece
from settings import *
import random
from board import Board
import time

# http://www.frayn.net/beowulf/theory.html#iterative
# https://blog.csdn.net/qq_24211837/article/details/121322017
# https://github.com/netcan/AnimalChess/blob/master/core/src/player/alpha_beta.rs

#先默认team0为电脑
def evaluation(board:Board) -> int:
    value = 0
    for piece in board.all_pieces()[0]:
        value += CHESS_SCORE[piece.value-1]
        value += POS_SCORE[piece.value-1][piece.pos[1]][piece.pos[0]]
    for piece in board.all_pieces()[1]:
        value -= CHESS_SCORE[piece.value-1]
        value -= POS_SCORE[piece.value-1][piece.pos[1]][piece.pos[0]]
    
    return value

def negamax(board:Board,depth:int,alpha:int,beta:int,sign:int) -> int:
    if depth == 0:
        return evaluation(board)

    else:
        possible_moves = board.get_next_steps(board.turn)
        for move in possible_moves:
            board.move(board.piece_on(move[0]),move[1])
            alpha = max(alpha, -negamax(board,depth-1,-beta,-alpha,-sign))
            board.undo_move()
            if alpha >= beta:
                break

    return alpha

def move(board:Board):
    best = -10000
    my_moves = []
    all_move = board.get_next_steps(board.turn)   
    for move in all_move:
        board.move(board.piece_on(move[0]),move[1])
        score = -negamax(board,3,-10000,10000,-1)
        board.undo_move()

        if score > best:
            best = score
            my_moves = [move]
        if score == best:
            my_moves.append(move)

        print(f"{move} done")
    move = random.choice(my_moves)
    print(f"========================mymove is {my_moves} =========================================")
    print(f"choice is {move}")
    return move





    
    


    