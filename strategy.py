from piece import Piece
from setting import *

def count_value(step):
    value = 0
    piece_pos = step[0]
    move_pos = step[1]
    me = Piece.get_piece(piece_pos)
    targat = Piece.get_piece(move_pos)
    value += me.value
    if targat:
        if me.value >= targat.value:
            value += 10
        if me.value < targat.value:
            value += 10
    if move_pos in HOME[not me.team]:
        value += 100
    return value

def choose_next_step(steps):
    valuelist = []
    for step in steps:
        valuelist.append(count_value(step))
    print(max(valuelist),steps[valuelist.index(max(valuelist))])
    return steps[valuelist.index(max(valuelist))]