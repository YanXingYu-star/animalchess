import sys
import pygame
import pygame_gui

from settings import *
from level import Level
from menu import Menu,Start_menu
import piece

class Game(object):
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((CELL_WIDTH*7+200, CELL_HEIGHT*9+2))
        pygame.display.set_caption('斗兽棋')
        self.clock = pygame.time.Clock()

        self.manager = pygame_gui.UIManager((CELL_WIDTH*7+200, CELL_HEIGHT*9+2),starting_language='zh')
        self.gui = Menu(self.manager)

        self.level = Level()
        self.start_menu_ = Start_menu()

        self.game_over = True    

    @property
    def controller(self):
        if self.game_over:
            return self.start_menu_
        else:
            return self.level

    def run(self):

        self.controller.game_over = self.game_over
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.controller.reponse_click(event.pos)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                print(1)
                self.controller.reponse_button(event.ui_element)
                print(id(event))    
            self.controller.manager.process_events(event)
        

        delta_time = self.clock.tick(20) / 1000
        self.controller.run(delta_time)

        self.game_over = self.controller.game_over
        pygame.display.update()
        

if __name__ == '__main__':
    game = Game()
    while True:
        game.run()