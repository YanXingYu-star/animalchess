import sys
import pygame
import pygame_gui

from settings import *
from level import Level
from menu import Menu
import piece

class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((CELL_WIDTH*7+200, CELL_HEIGHT*9))
        pygame.display.set_caption('斗兽棋')
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((CELL_WIDTH*7+200, CELL_HEIGHT*9),starting_language='zh')
        self.gui = Menu(self.manager)
        self.level = Level()
        self.game_over = True    

    def run(self):
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    piece.Piece.click_pos[0] = piece.Piece.convert_to_board(event.pos)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.gui.back_button:
                    self.game_over = True
                    self.level = Level()
                    print(self.level)
                    

            self.manager.process_events(event)
        
        delta_time = self.clock.tick(20) / 1000

        self.level.run()
        if self.level.game_over:
            self.game_over = True
            self.level.blit_game_over()
            self.level = Level()
            print(self.level)
        self.manager.update(delta_time)
        self.manager.draw_ui(self.screen)
        pygame.display.update()

    def start_menu(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.gui.start_button:
                    self.game_over = False
                    #print(self.game_over)
            self.manager.process_events(event)
        delta_time = self.clock.tick(20) / 1000
        self.screen.fill('white')
        self.manager.update(delta_time)
        self.manager.draw_ui(self.screen)
        pygame.display.update()
        

if __name__ == '__main__':
    game = Game()
    while True:
        if game.game_over:
            game.start_menu()
        else:
            game.run()
