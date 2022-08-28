import piece
from settings import *

def virtual_pos(me:piece.Piece,target_pos):
    x = target_pos[0]
    y = target_pos[1]
    value = 0
    for i in (x-1,x,x+1):
        if 0 <= i < len(piece.Piece.board):
            for j in (y-1,y,y+1):
                if 0<= j < len(piece.Piece.board[0]):
                    if (i,j) != me.pos:
                        print('aaaaaij'+str((i,j)))
                        if piece.Piece.piece_on((i,j)) and piece.Piece.piece_on((i,j)).team != me.team:
                            print('------' + str(piece.Piece.piece_on((i,j))))
                            if me.compare_value(piece.Piece.piece_on((i,j))) == me:
                                value -= me.value*0.7 + 2
                            else:
                                value += piece.Piece.piece_on((i,j)).value*0.5 + 2
                        else:
                            value += 0.01
    return value

def count_value(step):
    value = 0
    piece_pos = step[0]
    move_pos = step[1]
    me = piece.Piece.piece_on(piece_pos)
    targat = piece.Piece.piece_on(move_pos)
    value += me.value * 0.2
    value += virtual_pos(me,move_pos)
    return value

def choose_next_step(steps):
    valuelist = []
    for step in steps:
        valuelist.append(count_value(step))
    print(max(valuelist),steps[valuelist.index(max(valuelist))])
    return steps[valuelist.index(max(valuelist))]