import pygame
import json
import time
from copy import deepcopy

from settings import *
import piece
import board
import strategy


class Level(Controller):
    """ 完成单个棋局内各功能的调度 """

    def __init__(self):

        self.setup()
        self.graph_init()
        self.gui_init()

        self.player = [COMPUTER, HUMAN]  # [player1,player2]
        self.game_over = True

    @property
    def turn(self):
        """ 执棋的一方 """
        return self.board.turn

    def setup(self):
        # 创建棋盘
        self.board = board.Board(7, 9)

        # 创建棋子并添加至棋盘
        with open("piece.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        for i in data['piece']:
            self.board.add_piece(piece.Piece(i["name"], i["team"], *eval(i["pos"])))
        for i in data['lion_tiger']:
            self.board.add_piece(piece.LionTiger(i["name"], i["team"], *eval(i["pos"])))
        for i in data['mouse']:
            self.board.add_piece(piece.Mouse(i["name"], i["team"], *eval(i["pos"])))

    """ 图形界面 """
    def create_piece_sprites(self):
        self.piece_sprites = []
        for p in self.board.all_pieces()[2]:
            self.piece_sprites.append(piece.PieceSprite(
                self.all_sprites, p, self.board))

    def create_board_sprite(self):
        self.board_sprite = board.BoardSprite(self.all_sprites, self.board)

    def graph_init(self):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.Group()

        self.create_board_sprite()
        self.create_piece_sprites()

    def blit_game_over(self):
        self.display_surface.fill('white')
        game_over_surface = font.render("game over", True, "black", "white")
        self.display_surface.blit(game_over_surface, (0, 0))
        pygame.display.update()
        time.sleep(1)

    """ GUI """
    def gui_init(self):
        self.manager = pygame_gui.UIManager(
            (CELL_WIDTH*7+200, CELL_HEIGHT*9+2), starting_language='zh')
        self.back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((CELL_WIDTH*7+20, 0), (100, 50)),
                                                        text='退出游戏',
                                                        manager=self.manager)
    """ 运行 """
    def check_game_over(self):
        if self.board.winner:
            self.game_over = True
            self.__init__()

    def run(self, delta_time):
        self.display_surface.fill('white')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()
        self.check_game_over()

        if self.player[self.turn]:  # 如果执棋者是电脑
            step = strategy.move(deepcopy(self.board))
            self.board.move(self.board.piece_on(step[0]),step[1])

        self.manager.update(delta_time)
        self.manager.draw_ui(self.display_surface)

    def reponse_click(self, pos):
        if not self.player[self.turn]:  # 执棋者是人
            self.board.click_pos.append(self.board.convert_to_board(pos))
            self.board.reponse_click()

    def reponse_button(self, ui_element):
        if ui_element == self.back_button:
            self.game_over = True
            self.__init__()

