import pygame

# 字体
FONT = 'resource\msyh.ttf'
pygame.init()
font = pygame.font.Font(FONT, 30)

#颜色
#https://blog.csdn.net/weixin_44478378/article/details/104967241

""" BOARD """
animal = ["鼠", "猫", "狗", "狼", "豹", "虎", "狮", "象"]

RIVER: tuple = ((1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5),
                (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5))  # 储存的代表河水的坐标
TEAM = ("black", "red")
TRAP = (((2,0), (4,0), (3,1)), ((2, 8), (4, 8), (3, 7)))
HOME = ((3, 0), (3, 8))

MOVE_COMMAND = {'up':(-1,0),'down':(1,0),'left':(0,-1),'right':(0,1)}

""" COLOR """
WHITE = 255,255,255
RED = 255,0,0
GREEN = 0,255,0
BLUE = 0,0,255
BLACK = 0,0,0
GOLD = 255,251,0

RED_F = 31
BLUE_F = 34
BLUE_B = 44

""" Board """
BOARD_ROW = 9   #lxkr
BOARD_COLUMN = 7


""" window """
CELL_WIDTH ,CELL_HEIGHT = 50, 50
DETA_X = 7 #为了棋子居于各自中间的偏差量
DETA_Y = 5
