import sys
sys.path.append('.')

from time import sleep
import json
import re


from piece import Piece, Lion_tiger, Mouse
from setting import *
import play_in_terminal.terminal_print as terminal_print

""" 游戏初始化 """


def create_piece():
    """ 重置棋盘，创建棋子对象 """
    Piece.reboot()
    with open("piece.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    for i in data['piece']:
        Piece(i["name"], i["team"], *eval(i["pos"]))
    for i in data['lion_tiger']:
        Lion_tiger(i["name"], i["team"], *eval(i["pos"]))
    for i in data['mouse']:
        Mouse(i["name"], i["team"], *eval(i["pos"]))


def is_game_over():
    return Piece.game_over


""" 显示棋子 """


def print_piece():

    print('\x1b[9A')
    print('\x1b[6A]')
    print('  0  1  2  3  4  5  6 ')
    for row in range(len(Piece.get_board_matrix())):
        print(row, end=" ")
        for element in Piece.get_board_matrix()[row]:
            if element == 0:
                print('--', end=" ")
            elif element >= 0:
                print('\033[0;32;40m'+animal[element-1]+'\033[0m', end=' ')
            elif element < 0:
                element = -element
                print('\033[0;31;40m'+animal[element-1]+'\033[0m', end=' ')
        print('')


actor_team = 0


def move(command: str):
    global actor_team
    if command == 'esc':
        sys.exit()
    elif re.match('\d \d *', command):
        list_ = re.split(" ", command)
        move_array = MOVE_COMMAND[list_[2]]
        picked_pos = (int(list_[0]), int(list_[1]))
        target_pos = (picked_pos[0]+move_array[0], picked_pos[1]+move_array[1])
        if picked_pos in Piece.all_pos(actor_team):
            if target_pos in Piece.board[actor_team][picked_pos].passable_area:
                Piece.board[actor_team][picked_pos].move(target_pos)
                actor_team = not actor_team
            else:
                print('不可以走')
        else:
            print('该位置无可选棋子')
    else:
        print('command error')


""" 终端光标控制 """


def up(row):
    for i in range(row//9):
        print('\x1b[9A')
    else:
        print('\x1b[%dA' % (row % 9))


if __name__ == "__main__":
    create_piece()
    print('\x1b[2J')
    while True:
        print_piece()
        command = input('请输入指令：')
        move(command)
