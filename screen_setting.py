""" 该模块封装了pygame的几个函数 """

import pygame
from pygame import display, time, font, draw

from pygame import event as pygame_event
import sys
from setting import *
from typing import Tuple


pygame.init()
clock = time.Clock()
font = font.Font(FONT, 30)
clock_time = clock.tick_busy_loop(60)


""" 事件处理 """

def event_check(func):
    def inner():
        for event in pygame_event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print('pos is')
                    print(event.pos)
                    func(event.pos)
    return inner


""" 图像显示 """
screen = display.set_mode((CELL_WIDTH*7+200, CELL_HEIGHT*9))
display.set_caption("斗兽棋")


def blit_text(text: str, pos: tuple, color=BLACK, background=WHITE):
    """ 用pygame.font显示文字 """
    t = font.render(text, True, color,
                    background)  # render(text, antialias, color, background=None)
    screen.blit(t, pos)
    return t.get_size()


def get_text_size(text):
    t = font.render(text, True, BLACK, WHITE)  # render(text)
    return t.get_size()


def blit_rect(color, rect: Tuple[int, int, int, int], width):
    draw.rect(screen, color, rect, width)


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


class Surface_(object):
    def __init__(self, size, super_surface: pygame.Surface = screen, pos=(0, 0)):
        self.size = size
        self.surface: pygame.Surface = pygame.Surface(size)
        self.super_surface = super_surface
        self.pos = pos 

    def blit_me(self):
        self.super_surface.blit(self.surface,self.pos)
        pass

    def blit_text(self, text: str, pos: tuple, color=BLACK, background=WHITE):
        """ 显示文字 """
        t = font.render(
            text, True, color, background)  # render(text, antialias, color, background=None)
        self.surface.blit(t, pos)
        self.blit_me()

    @staticmethod
    def get_text_size(text):
        """ 获取显示要文字的尺寸 """
        t = font.render(text, True, BLACK, WHITE)  # render(text)
        return t.get_size()

    def blit_rect(self, color, rect: Tuple[int, int, int, int], width):
        draw.rect(self.surface, color, rect, width)
        self.blit_me()

    def update(self,func):
        def inner():
            self.surface.fill(WHITE)
            func()
            display.update()
        return inner

window:Surface_ = Surface_((0,0))
window.surface = screen
window.size = screen.get_size()

class Button(object):
    def __init__(self, pos, text, switch=None):
        self.text = text   #
        # 按键的矩形(left,top,width,height)
        self.rect = pos + get_text_size(self.text)
        self.status = 1  # 1：按钮可以按
        self.open = 0  # 1：按钮开启 0：按钮关闭
        self.switch = switch  # Button关联的变量
        print(self.rect)

    def open_me(self):
        self.open = not self.open
        if self.switch != None:
            self.switch.reponse_click()

    def pos_in_rect(self, pos):
        if pos[0] > self.rect[0] and pos[0] < self.rect[0]+self.rect[2]:
            if pos[1] > self.rect[1] and pos[1] < self.rect[1]+self.rect[3]:
                return True
        else:
            return False

    def is_click(self, click_pos):
        if self.status == 0:
            return False
        else:
            if self.pos_in_rect(click_pos):  # 判断pos是否在self.rect内
                self.open_me()
            return self.pos_in_rect(click_pos)

    def check_click(self, pos):

        return self.is_click(pos)

    @property
    def blit_parameter(self):
        """ 返回pygame.blit所需的一些参数 """
        return (self.text, self.rect)

    def blit(self):
        fill_background()
        blit_rect(BLACK, self.rect, 1)
        blit_text(*self.blit_parameter)
        update()
