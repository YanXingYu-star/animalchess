import piece
from settings import *
import random
import board
import time



""" -------------------------------------------------------------------------------------------------- """

#TODO
""" def minimax(board:board.Board,player,next_player,alpha=-10000,beta=20000,depth = 3):

    if board.check_winner(board.pos_list) == TEAM[1]:  # 电脑胜利
        return +1000
    elif board.check_winner(board.pos_list) == TEAM[0]:     # 人类胜利
        return -1000
    if board.capture:
        if board.capture.team == COMPUTER:
            return board.capture.value * -10
        if board.capture.team == HUMAN:
            return board.capture.value * 10


    
    if depth:
        all_move = board.get_next_steps(board.turn)   
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
        return beta """

def move(board:board.Board,alpha = -10000,beta = 10000):
    best = -10000
    my_moves = []
    all_move = board.get_next_steps(board.turn)   
    for move in all_move:
        move_piece = board.piece_on(move[0])
        board.move(move_piece,move[1])
        score = minimax(board,3,1)
        board.undo_move()

        if score > best:
            best = score
            my_moves = [move]
        if score == best:
            my_moves.append(move)

        if score >beta:
            break
        print(f"{move} done")
        time.sleep(1)
    move = random.choice(my_moves)
    print(f"========================mymove is {my_moves} =========================================")
    print(f"choice is {move}")
    return move


def minimax(board:board.Board,depth,my_team,max_level:bool = True,alpha = -10000,beta = 10000):
    """ 极大极小值算法 """



    if board.check_winner(board.pos_list) == TEAM[my_team]:
        return 10000
    if board.check_winner(board.pos_list) == TEAM[not my_team]:
        return -10000
    if board.capture:
        if board.capture.team == my_team:
            return board.capture.value * -10
        if board.capture.team != my_team:
            return board.capture.value * 10

    if depth:
        for move in board.get_next_steps(board.turn):
            move_piece = board.piece_on(move[0])
            board.move(move_piece,move[1])
            value = minimax(board,depth-1,my_team,not max_level)
            board.undo_move()

            if max_level:
                if value > alpha:
                    alpha = value
                if alpha > beta:
                    return beta
            else:
                if value < beta:
                    beta = value
                if alpha > beta:
                    return alpha

    if max_level:
        return alpha
    else:
        return beta


    
    


    