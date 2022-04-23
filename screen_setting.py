""" 该模块封装了pygame的几个函数 """
import pygame
import sys
from setting import *
from typing import Tuple


pygame.init()
screen = pygame.display.set_mode((50*7+200, 50*9))
pygame.display.set_caption("斗兽棋")
clock = pygame.time.Clock()
font = pygame.font.Font('msyh.ttf', 30)
clock_time = clock.tick_busy_loop(60) 


""" 事件处理 """

def event_check(*fun_reponse_click):
    """ 响应鼠标点击，传入一个包含处理函数的列表 """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print('pos is')
                print(event.pos)
                for fun in fun_reponse_click:
                    fun(event.pos)

def outter(func):
    pass

""" 图像显示 """


def blit_text(text:str,pos:tuple,color=BLACK,background=WHITE):
    """ 用pygame.font显示文字 """
    t = font.render(text,True,color,background) # render(text, antialias, color, background=None)
    screen.blit(t,pos)

def blit_rect(background_color,rect:Tuple[int,int,int,int],width):
    pygame.draw.rect(screen,background_color,rect,width)

def fill_background():
    screen.fill(WHITE) 

def update():
    pygame.display.update()

def screen_update(func):
    def inner():
        screen.fill(WHITE)
        func()
        pygame.display.update()
    return inner




