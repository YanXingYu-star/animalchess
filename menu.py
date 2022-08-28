import pygame_gui
import pygame

from settings import *

class Menu(object):
    def __init__(self,manager):
        self.manager = manager
        
        self.setup()
    
    def setup(self):
        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((CELL_WIDTH*7+20, 0), (100, 50)),
                                                        text='退出游戏',
                                                        manager=self.manager)
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((CELL_WIDTH*7+20, 50), (100, 50)),
                                                        text='开始游戏',
                                                        manager=self.manager)   