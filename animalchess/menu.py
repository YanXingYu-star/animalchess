import pygame_gui
import pygame

from settings import *
class Start_menu(Controller):
    """ 构建开始菜单 """
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.manager = pygame_gui.UIManager(WINDOW_SIZE,starting_language='zh')
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