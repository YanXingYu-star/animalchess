import piece
from settings import *
import random
import board



""" -------------------------------------------------------------------------------------------------- """

#TODO
def minimax(board:board.Board,player,next_player,alpha=-10000,beta=20000,depth = 3):

    if board.check_winner(board.pos_list) == "team1":  # 电脑胜利
        return +1000
    elif board.check_winner(board.pos_list) == "team0":     # 人类胜利
        return -1000
    if board.capture:
        if player == COMPUTER:
            return board.capture.value * -10
        if player == HUMAN:
            return board.capture.value * 10


    all_move = board.get_next_steps(board.turn)   
    if depth:
        for move in all_move:   #move:[from_pos,target_pos]
            move_piece = board.piece_on(move[0])
            board.move(move_piece,move[1])
            val = minimax(board,next_player,player,alpha,beta,depth-1)
            board.undo_move()

            if player == COMPUTER:
                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha

    if player == COMPUTER:
        return alpha
    else:
        return beta

def move(board:board.Board):
    best = -10000
    my_moves = []
    all_move = board.get_next_steps(board.turn)   
    for move in all_move:
        move_piece = board.piece_on(move[0])
        board.move(move_piece,move[1])
        score = minimax(board,HUMAN,COMPUTER)
        board.undo_move()

        if score > best:
            best = score
            my_moves = [move]
        if score == best:
            my_moves.append(move)

    move = random.choice(my_moves)
    print(f"========================mymove is {my_moves} =========================================")
    print(f"choice is {move}")
    return move


    
    