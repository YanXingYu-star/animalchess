import pygame
import pygame_gui
from abc import ABCMeta, abstractmethod

# 字体
FONT = 'resource/msyh.ttf'
pygame.init()
font = pygame.font.Font(FONT, 30)

""" BOARD """
animal = ["鼠", "猫", "狗", "狼", "豹", "虎", "狮", "象"]

RIVER: tuple = ((1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5),
                (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5))  # 储存的代表河水的坐标
TEAM = ("black", "red")
TRAP = (((2,0), (4,0), (3,1)), ((2, 8), (4, 8), (3, 7)))
HOME = ((3, 0), (3, 8))

BOARD_ROW = 9   
BOARD_COLUMN = 7


""" window """
CELL_WIDTH ,CELL_HEIGHT = 50, 50
WINDOW_SIZE = (CELL_WIDTH*7+200, CELL_HEIGHT*9+2)   #窗口大小
DETA_X = 7 #为了棋子居于各自中间的偏差量
DETA_Y = 5

class Controller(metaclass = ABCMeta):
    """ 负责游戏某一进程的控制器 """
    def __init__(self):
        pass

    @abstractmethod
    def reponse_click(self):
        """ 响应点击 """
        pass

    @abstractmethod
    def reponse_button(self):
        """ 响应按钮 """
        pass

    @abstractmethod
    def run(self):
        pass

#MOVE_COMMAND = {'up':(-1,0),'down':(1,0),'left':(0,-1),'right':(0,1)}

HUMAN = 0
COMPUTER = 1