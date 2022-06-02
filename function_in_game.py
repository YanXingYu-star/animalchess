""" 对局进行中的函数 """

from time import sleep
import json
import random

import piece
from piece import Piece,Lion_tiger,Mouse
import screen_setting as sset
from setting import *
import strategy

""" 游戏初始化 """
def create_piece():
    """ 重置棋盘，创建棋子对象 """
    Piece.reboot()
    with open("piece.json", "r",encoding="utf-8") as f:
        data = json.load(f)    
    for i in data['piece']:
        Piece(i["name"],i["team"],*eval(i["pos"]))
    for i in data['lion_tiger']:
        Lion_tiger(i["name"],i["team"],*eval(i["pos"]))
    for i in data['mouse']:
        Mouse(i["name"],i["team"],*eval(i["pos"]))

def is_game_over():
    return Piece.game_over


""" 图形绘制 """
board_surface = sset.Surface_((7*CELL_WIDTH, 9*CELL_HEIGHT))
informations_surface = sset.Surface_((200,CELL_HEIGHT*9),pos = (7*CELL_WIDTH, 0))

def draw_river():
    for pos in RIVER:
        board_surface.blit_rect(BLUE,(pos[1]*50, pos[0]*50,50,50),0)

def draw_trap(): 
    for t in TRAP:
        for pos in t:       
            board_surface.blit_text("陷",(pos[1]*50+DETA_X, pos[0]*50+ DETA_Y),BLUE)

def draw_home():
    for pos in HOME:
        board_surface.blit_text("穴",(pos[1]*50+ DETA_X, pos[0]*50+ DETA_Y),BLUE)

def draw_checkerboard():
    """ 绘制棋盘 """
    for x in range(7):
        for y in range(9):
            board_surface.blit_rect(BLACK, (x*50, y*50, 50, 50), 1)
    draw_river()
    draw_trap()
    draw_home()

def draw_choice():
    """ 画选中棋子的金框 """
    if Piece.get_piece_picked():
        pos = Piece.get_piece_picked().real_pos
        board_surface.blit_rect(GOLD,(pos[0], pos[1], 50, 50),3)

def turn():
    pos = (50,50)
    if actor_team:
        text = "轮到红方"
    else:
        text = "轮到黑方"
    return text,pos

@informations_surface.update
def blit_information():
    informations_surface.blit_text(*turn())

@board_surface.update
def blit_game_screen():
    """ 绘制棋子 """
    draw_checkerboard()
    for a_piece in piece.Piece.all_piece():    #依次绘制各棋子
        board_surface.blit_text(a_piece.name,a_piece.blit_pos,TEAM[a_piece.team])
    draw_choice()
    blit_information()

def blit_game_over():
    sset.fill_background()
    sset.blit_text("Game Over",(200,150))
    sset.update()
    sleep(1)





""" 事件响应 """
actor_team = 0


""" 人机 """
def robot_act():
    global actor_team
    #next_step = random.choice(Piece.get_next_steps(actor_team))
    next_step = strategy.choose_next_step(Piece.get_next_steps(actor_team))
    Piece.board[actor_team][next_step[0]].move(next_step[1])
    actor_team = not actor_team


@sset.event_check
def reponse_click(pos):

        """ 响应鼠标在棋盘内的点击
        pos : 行列数
         """
        global actor_team
        pos = Piece.convert_to_board(pos)

        pos = tuple(reversed(pos))
        print("点击位置为{}".format(pos))
        print(Piece.all_pos(actor_team))  

        if not Piece.get_piece_picked():

            if pos in Piece.all_pos(actor_team):
                print(Piece.all_pos(actor_team))    
                Piece.set_piece_picked(Piece.board[actor_team][pos])
                print("被选中的棋子是"+Piece.get_piece_picked().name)
                print("它可走的位置是", Piece.get_piece_picked().passable_area)
        else:

            if pos in Piece.get_piece_picked().passable_area:  # 点击坐标在传入棋子的可行动范围内，移动棋子，轮换执棋
                Piece.get_piece_picked().move(pos)
                Piece.clear_piece_picked()
                actor_team = not actor_team
                print(Piece.get_piece_picked())
                robot_act()

            elif pos == Piece.get_piece_picked()._pos:  # 点击正选中的棋子，取消选中
                Piece.clear_piece_picked()
            
            elif pos in Piece.all_pos(actor_team):  # 选中己方其他棋子，选中该棋子
                Piece.set_piece_picked(Piece.board[actor_team][pos])



