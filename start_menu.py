"""该模块用于构建开始菜单 """
from button import *

game_start = Switch()
start_button = Button((400,50,100,50),"开始游戏",game_start)

def blit_start_screen():
    start_button.blit()

game_pause = Switch()
pause_button = Button((400,150,100,50),"暂停游戏",game_pause)