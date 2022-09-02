import pygame
import json
import time

from settings import *
import piece
import board


class Level(object):
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.piece_sprites = TestGroup()

        self.setup()

        self.game_over = False

    def setup(self):
        # 创建棋盘
        self.board = board.Board(self.all_sprites, 7, 9)

        # 创建棋子
        piece.Piece.reset()
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
        if piece.Piece.game_over[0]:
            self.game_over = True

    def blit_game_over(self):
        self.display_surface.fill('white')
        game_over_surface = font.render("game over",True,"black","white")
        self.display_surface.blit(game_over_surface,(0,0))
        pygame.display.update()
        time.sleep(1)
            

    def run(self):
        self.display_surface.fill('white')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()
        self.piece_sprites.draw(self.display_surface)
        self.piece_sprites.update()
        self.check_game_over()


class TestGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def update(self, *args, **kwargs):
        for sprite in self.sprites(): 
            if sprite != sprite.piece_picked[0]:
                sprite.update(*args, **kwargs)
        for sprite in self.sprites():
            if sprite == sprite.piece_picked[0]:
                sprite.update(*args, **kwargs)