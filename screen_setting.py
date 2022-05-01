""" 该模块封装了pygame的几个函数 """
import pygame
from pygame import display,time,font,draw
from pygame import event as pygame_event    #只是为了找到pygame内部moudle，不然运行前很多pygame类的实例无法显示其类型
import sys
from setting import *
from typing import Tuple


pygame.init()
screen = display.set_mode((50*7+200, 50*9))
display.set_caption("斗兽棋")
clock = time.Clock()
font = font.Font('msyh.ttf', 30)
clock_time = clock.tick_busy_loop(60) 


""" 事件处理 """

def event_check(*fun_reponse_click):
    """ 响应鼠标点击，传入一个包含处理函数的列表 """
    for event in pygame_event.get():
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
    draw.rect(screen,background_color,rect,width)

def fill_background():
    screen.fill(WHITE) 

def update():
    display.update()

def screen_update(func):
    def inner():
        screen.fill(WHITE)
        func()
        display.update()
    return inner




