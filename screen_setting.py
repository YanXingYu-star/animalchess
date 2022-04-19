""" 该模块提供了与pygame进行交互的接口 """
import pygame
import sys
import piece
import function_in_game as fun
import start_interface
from time import sleep
from setting import *
from typing import Tuple


pygame.init()
screen = pygame.display.set_mode((50*7+200, 50*9))
pygame.display.set_caption("斗兽棋")
clock = pygame.time.Clock()
font = pygame.font.Font('msyh.ttf', 30)
clock_time = clock.tick_busy_loop(60) 

trap_text = font.render("陷", True, (0,0,255), (255,255,255))    #render(text, antialias, color, background=None)
home_text = font.render("穴",True, (0,0,255), (255,255,255))

""" 事件处理 """

def event_check(*fun_reponse_click):
    """ 响应鼠标点击，传入一个包含处理函数的列表 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for fun in fun_reponse_click:
                    fun(event.pos)


""" 图像显示 """


def blit_text(text:str,pos:tuple,color=BLACK,background=WHITE):
    """ 用pygame.font显示文字 """
    t = font.render(text,True,color,background) # render(text, antialias, color, background=None)
    screen.blit(t,pos)

def blit_rect(background_color,rect:Tuple[int,int,int,int],width):
    pygame.draw.rect(screen,background_color,rect,width)

def blit_game_screen():
    """ 绘制棋子 """
    screen.fill(WHITE) 
    fun.draw_checkerboard()
    for a_piece in piece.Piece.all_piece():    #依次绘制各棋子
        blit_text(a_piece.name,a_piece.real_pos,TEAM[a_piece.team])

    fun.draw_choice()
    blit_text(*fun.turn())
    pygame.display.update()

def blit_start_screen():
    screen.fill(WHITE) 
    screen.blit(*start_interface.start_button.blit_parameter())  
    pygame.display.update()


def blit_game_over():
    screen.fill(WHITE)
    blit_text("Game Over",(200,150))
    pygame.display.update()
    sleep(1)