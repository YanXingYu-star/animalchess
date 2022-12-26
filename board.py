from typing import List, Dict, Tuple
import pygame
from settings import *
from piece import Piece

font = pygame.font.Font(FONT, 30)


class Board(object):
    """ Board类
        储存棋盘信息
        提供响应鼠标点击、移动棋子、判断胜负等方法"""

    def __init__(self, group, width, height):
        self.group = group
        self.width = width  # 横向的格数
        self.height = height
        self.sprite = BoardSprite(self.group, self.width, self.height)

        self.pos_list = [{}, {}]  # [team1dict{pos:Piece},{}]
        self._piece_picked = None
        self.turn = 0
        self.click_pos = []
        self.winner = []

    @property
    def piece_picked(self):
        return self._piece_picked

    @piece_picked.setter
    def piece_picked(self,piece:Piece):
        if self._piece_picked:
            self._piece_picked.choosen = False

        self._piece_picked = piece
        if self._piece_picked:
            self._piece_picked.choosen = True


        return self.piece_picked

    def check_winner(self,pos_list):
        print(111)
        if (3,0) in pos_list[1].keys() or not pos_list[0]:
            print("team1")
            return "team1"
        if (3,8) in pos_list[0].keys() or (not pos_list[1]):
            
            print("team2")
            return "team0"


    def move(self, piece:Piece, pos):
        self.pos_list[piece.team].pop(piece.pos,0) 
        piece.pos = pos
        self.pos_list[piece.team][piece.pos] = piece

        self.pos_list[not piece.team].pop(piece.pos,1)

        self.turn = not self.turn
        print(f"turn to {self.turn}")

        if self.check_winner(self.pos_list):
            self.winner.append(self.check_winner(self.pos_list))

    def reponse_click(self):
        if self.click_pos:
            pos = self.click_pos.pop()
            print(f"{self.turn} 方执棋")
            if not self.piece_picked:
                if pos in self.all_pos()[self.turn]:
                    #print(Piece.all_pos(actor_team)) 
                    self.piece_picked = self.piece_on(pos)
                print(1.1)
            else:
                print(2)
                if pos in self.piece_picked.get_passable_area(self):  # 点击坐标在传入棋子的可行动范围内，移动棋子，轮换执棋
                    self.move(self.piece_picked,pos)
                    self.piece_picked = None
                    print(2.1)
                elif pos == self.piece_picked.pos:  # 点击正选中的棋子，取消选中
                    self.piece_picked = None
                    print("2.2")
                elif pos in self.all_pos()[self.turn]:  # 选中己方其他棋子，选中该棋子
                    self.piece_picked = self.piece_on(pos)
                    print("2.3")


    def all_pos(self) -> Tuple[List]:
        """ 返回指定队伍棋子的坐标 """
        team0_pos = list(self.pos_list[0].keys())
        team1_pos = list(self.pos_list[1].keys())
        return team0_pos, team1_pos, team0_pos + team1_pos

    def all_piece(self) -> Tuple[List[Piece]]:
        """ 返回包含所有棋子的元组 """
        team0_pieces = list(self.pos_list[0].values())
        team1_pieces = list(self.pos_list[1].values())
        return team0_pieces, team1_pieces, team0_pieces + team1_pieces

    def piece_on(self, pos) -> 'Piece':
        """ 通过传入坐标返回棋子对象 """
        if pos in self.all_pos()[0]:
            return self.pos_list[0][pos]
        elif pos in self.all_pos()[1]:
            return self.pos_list[1][pos]
        else:
            return None

    def get_next_steps(self, turn) -> List[tuple]:  # TODO
        """ 获取可走的下一步棋 """
        next_steps = []
        for piece in self.all_piece()[turn]:
            next_steps += map(lambda pos: (piece.pos, pos),
                              piece.get_passable_area(self))
        return next_steps


class BoardSprite(pygame.sprite.Sprite):
    """ 渲染棋盘 """
    def __init__(self, group, width, height):
        super().__init__(group)
        self.width = width  # 横向的格数
        self.height = height

        self.image = pygame.Surface((width * 50, height * 50))
        self.rect = self.image.get_rect()
        self.draw_board()

    def draw_board(self):
        """ 绘制棋盘 """

        self.image.fill('white')

        # 画格子
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(self.image, "black", (x * 50, y * 50, 50, 50), 1)

        # 河流
        for pos in RIVER:
            pygame.draw.rect(self.image, "deepskyblue", (pos[0] * 50, pos[1] * 50, 50, 50), 0)
        # 陷阱
        for t in TRAP:
            for pos in t:
                trap_surface = font.render("陷", True, "blue", "white")
                self.image.blit(trap_surface, (pos[0] * 50 + DETA_X, pos[1] * 50 + DETA_Y))

        # 兽穴
        for pos in HOME:
            home_surface = font.render("穴", True, "blue", "white")
            self.image.blit(home_surface, (pos[0] * 50 + DETA_X, pos[1] * 50 + DETA_Y))

    def update(self):
        pass

