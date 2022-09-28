import pygame_gui
import pygame

from settings import *

uimanager = pygame_gui.UIManager((CELL_WIDTH*7+200, CELL_HEIGHT*9+2),starting_language='zh')

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

class Start_menu(Controller):
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.manager = pygame_gui.UIManager((CELL_WIDTH*7+200, CELL_HEIGHT*9+2),starting_language='zh')
        self.start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((CELL_WIDTH*7+20, 50), (100, 50)),
                                                text='开始游戏',
                                                manager=self.manager)   

        self.game_over = True
    def reponse_click(self,pos):
        pass

    def reponse_button(self,ui_element):
        if ui_element == self.start_button:
            self.game_over = False
            print("back")

    def run(self,delta_time):
        self.display_surface.fill('white')
        self.manager.update(delta_time)
        self.manager.draw_ui(self.display_surface)