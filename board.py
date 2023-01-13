from typing import List, Dict, Tuple
import pygame
from settings import *
from piece import Piece

font = pygame.font.Font(FONT, 30)


class Board(object):
    """ Board类
        储存棋盘信息
        提供响应鼠标点击、移动棋子、判断胜负等方法"""

    def __init__(self, width, height):
        self.width = width  # 横向的格数
        self.height = height
        self.pos_list = [{}, {}]  # [team1dict{pos:Piece},{}]
        self._piece_picked = None
        self.turn = 0
        self.click_pos = []
        self.winner = []
        self.move_list = []

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
        if (3,0) in pos_list[1].keys() or not pos_list[0]:
            return TEAM[1]
        if (3,8) in pos_list[0].keys() or (not pos_list[1]):
            return TEAM[0]



    def move(self, piece:Piece, target_pos):
        """ 移动棋子 """
        from_pos = piece.pos
        self.pos_list[piece.team].pop(piece.pos,0)
        piece.pos = target_pos
        self.pos_list[piece.team][piece.pos] = piece

        captured_piece = self.pos_list[not piece.team].pop(piece.pos,0)
        self.capture = captured_piece
        self.turn = not self.turn
        

        #if self.check_winner(self.pos_list):
            #self.winner.append(self.check_winner(self.pos_list))

        self.move_list.append({"from_pos":from_pos,"target_pos":target_pos,"move_piece":piece,"captured_piece":captured_piece})
        return {"from_pos":from_pos,"target_pos":target_pos,"move_piece":piece,"captured_piece":captured_piece}

    def undo_move(self):
        """ 撤销移动 """
        move = self.move_list.pop() #dict
        from_pos = move["from_pos"]
        target_pos = move["target_pos"]
        move_piece = move["move_piece"]
        captured_piece = move["captured_piece"]

        self.pos_list[move_piece.team].pop(move_piece.pos,0) 
        self.pos_list[move_piece.team][from_pos] = move_piece
        move_piece.pos = from_pos

        if captured_piece:
            self.pos_list[captured_piece.team][target_pos] = captured_piece
            captured_piece.pos = target_pos

        self.turn = not self.turn

    def reponse_click(self):
        if self.click_pos:
            pos = self.click_pos.pop()
            if not self.piece_picked:
                if pos in self.all_pos()[self.turn]:
                    self.piece_picked = self.piece_on(pos)
            else:
                if pos in self.piece_picked.get_passable_area(self):  # 点击坐标在传入棋子的可行动范围内，移动棋子，轮换执棋
                    self.move(self.piece_picked,pos)
                    self.piece_picked = None
                elif pos == self.piece_picked.pos:  # 点击正选中的棋子，取消选中
                    self.piece_picked = None
                elif pos in self.all_pos()[self.turn]:  # 选中己方其他棋子，选中该棋子
                    self.piece_picked = self.piece_on(pos)


    def all_pos(self) -> Tuple[List]:
        """ 返回指定队伍棋子的坐标 """
        team0_pos = list(self.pos_list[0].keys())
        team1_pos = list(self.pos_list[1].keys())
        return team0_pos, team1_pos, team0_pos + team1_pos

    def all_pieces(self) -> Tuple[List[Piece]]:
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
        for piece in self.all_pieces()[turn]:
            next_steps += map(lambda pos: (piece.pos, pos),
                              piece.get_passable_area(self))
        return next_steps

    def add_piece(self,piece:Piece):
        """ 将棋子添加到棋盘 """
        self.pos_list[piece.team][piece.pos] = piece

    @staticmethod
    def convert_to_board(window_pos):
        """ 将窗口坐标转换为棋盘坐标 """
        return window_pos[0]//50, window_pos[1]//50


class BoardSprite(pygame.sprite.Sprite):
    """ 渲染棋盘 """
    def __init__(self, group,board:Board):
        super().__init__(group)
        self.width = board.width  # 横向的格数
        self.height = board.height

        self.image = pygame.Surface((self.width * 50, self.height * 50))
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

