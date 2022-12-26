import pygame
import json
import time

from settings import *
import piece
import board
import strategy

class Level(Controller):
    """ 完成棋局内各个功能的调度 """
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.piece_sprites = pygame.sprite.Group()

        self.setup()

        self.player = [HUMAN,HUMAN] #[player1,player2]

        self.game_over = True


        """ GUI """
        self.manager = pygame_gui.UIManager((CELL_WIDTH*7+200, CELL_HEIGHT*9+2),starting_language='zh')
        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((CELL_WIDTH*7+20, 0), (100, 50)),
                                                        text='退出游戏',
                                                        manager=self.manager)
    
    @property
    def turn(self):
        """ 执棋的一方 """
        return self.board.turn

    def setup(self):
        # 创建棋盘
        self.board = board.Board(self.all_sprites, 7, 9)

        # 创建棋子
        piece.Piece.reset(self.board)
        with open("piece.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for i in data['piece']:
            piece.Piece(self.piece_sprites,
                        i["name"], i["team"], *eval(i["pos"]))
        for i in data['lion_tiger']:
            piece.LionTiger(self.piece_sprites,
                             i["name"], i["team"], *eval(i["pos"]))
        for i in data['mouse']:
            piece.Mouse(self.piece_sprites,
                        i["name"], i["team"], *eval(i["pos"]))

    def check_game_over(self):
        if self.board.winner:
            self.game_over = True
            self.__init__()

    def blit_game_over(self):
        self.display_surface.fill('white')
        game_over_surface = font.render("game over",True,"black","white")
        self.display_surface.blit(game_over_surface,(0,0))
        pygame.display.update()
        time.sleep(1)
            

    def run(self,delta_time):
        self.display_surface.fill('white')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()
        self.piece_sprites.draw(self.display_surface)
        self.piece_sprites.update()
        self.check_game_over()

        if self.player[self.turn]: #如果执棋者是电脑
            print("电脑走棋") #TODO
            step = strategy.choose_next_step(self.board.get_next_steps(self.board.turn))
            piece.Piece.piece_on(step[0]).pos = step[1]
            
        self.manager.update(delta_time)
        self.manager.draw_ui(self.display_surface)


    def reponse_click(self,pos):
        if not self.player[self.turn]: #执棋者是人
            self.board.click_pos.append(piece.Piece.convert_to_board(pos))
            self.board.reponse_click()
    def reponse_button(self,ui_element):
        if ui_element == self.back_button:
            self.game_over = True
            self.__init__()
            print("back")


""" class TestGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        for sprite in self.sprites(): 
            if sprite != sprite.piece_picked[0]:
                sprite.update(*args, **kwargs)
        for sprite in self.sprites():
            if sprite == sprite.piece_picked[0]:
                sprite.update(*args, **kwargs) """