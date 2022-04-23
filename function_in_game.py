""" 对局进行中的函数 """
import piece
from piece import Piece,Lion_tiger,Mouse
import json
import screen_setting as sset
from setting import *
from time import sleep

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


""" 图形绘制 """

def draw_river():
    for pos in RIVER:
        sset.blit_rect(BLUE,(pos[0]*50, pos[1]*50,50,50),0)

def draw_trap(): 
    for t in TRAP:
        for pos in t:       
            sset.blit_text("陷",(pos[0]*50, pos[1]*50),BLUE)

def draw_home():
    for pos in HOME:
        sset.blit_text("穴",(pos[0]*50, pos[1]*50),BLUE)

def draw_checkerboard():
    """ 绘制棋盘 """
    for x in range(7):
        for y in range(9):
            sset.blit_rect(BLACK, (x*50, y*50, 50, 50), 1)
    draw_river()
    draw_trap()
    draw_home()

def draw_choice():
    """ 画选中棋子的金框 """
    if Piece.get_piece_picked() != 0:
        pos = Piece.get_piece_picked().real_pos
        sset.blit_rect(GOLD,(pos[0], pos[1], 50, 50),3)

def turn():
    pos = (400,50)
    if Piece.turn:
        text = "轮到红方"
    else:
        text = "轮到黑方"
    return text,pos

@sset.screen_update
def blit_game_screen():
    """ 绘制棋子 """
    draw_checkerboard()
    for a_piece in piece.Piece.all_piece():    #依次绘制各棋子
        sset.blit_text(a_piece.name,a_piece.real_pos,TEAM[a_piece.team])
    draw_choice()
    sset.blit_text(*turn())


def blit_game_over():
    sset.fill_background()
    sset.blit_text("Game Over",(200,150))
    sset.update()
    sleep(1)

def reponse_click(pos):
    print(pos)
    if pos[0] <= (50*7):
        pos = Piece.convert_to_board(pos)
        Piece.reponse_click(pos)



