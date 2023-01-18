""" 该模块包含Piece类和其两个子类"""
from typing import List, Dict, Tuple
from settings import *
import pygame


class Piece(object):
    """ Piece类
        储存单个棋子的位置、队伍、价值等信息，提供计算棋子可走位置的方法"""


    def __init__(self, name:str, team: bool, *pos):
        self._pos = pos  # pos为行列数,左上角为0,0
        self.team = team  # team传入0或1
        self.name = name
        self._value = animal.index(self.name)+1  # 用ANIMAL列表中的顺序来代表棋子的价值，用来判断吃子
        self.choosen = False

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        """ 将self._pos更新至cls.board """
        self._pos = pos
        return self.pos

    @property
    def value(self):
        if self.pos in TRAP[not self.team]:  # 敌方陷阱中的棋子价值为0
            return 0
        else:
            return self._value

    def compare_value(self, target_piece: 'Piece'):
        """ 比较两棋子的价值，返回价值较小的棋子 """
        # 老鼠吃大象
        if self.value == 1 and target_piece.value == 8:
            return target_piece
        elif self.value == 8 and target_piece.value == 1:
            return self
        # 大吃小
        elif self.value >= target_piece.value:
            return target_piece
        elif self.value < target_piece.value:
            return self

    def get_passable_area(self, board) -> list:
        """ 返回包含可移动的位置的列表"""
        self._passable_area = []  # 重置target_area

        def get(*pos: tuple):
            # 避开河流和己方棋子
            if pos not in RIVER and pos not in board.all_pos()[self.team] and 0 <= pos[0] <= 6 and 0 <= pos[1] <= 8 and pos != HOME[self.team]:
                if not(pos in board.all_pos()[not self.team] and self.compare_value(board.piece_on(pos)) == self):

                    self._passable_area.append(pos)
        get(self._pos[0], self._pos[1]+1)
        get(self._pos[0], self._pos[1]-1)
        get(self._pos[0]+1, self._pos[1])
        get(self._pos[0]-1, self._pos[1])

        return self._passable_area


class LionTiger(Piece):

    def __init__(self, name, team, *pos):
        super(LionTiger, self).__init__(name, team, *pos)

    def river_passable(self, pos, board):
        """ 检查是否有老鼠隔在河道中 """
        deta_x = (self.pos[0]-pos[0])
        if deta_x:
            dir_x = (pos[0]-self.pos[0])/abs(self.pos[0]-pos[0])
            for i in range(1, 3):
                if board.piece_on((self.pos[0]+i*dir_x, self.pos[1])):
                    return None
        else:
            dir_y = (pos[1]-self.pos[1])/abs(self.pos[1]-pos[1])
            for i in range(1, 4):
                if board.piece_on((self.pos[0], self.pos[1]+i*dir_y)):
                    return None
        return True

    def get_passable_area(self, board):
        """ 获取能移动的位置 """
        self._passable_area = []  # 重置target_area

        def get(*pos: tuple):
            # 避开己方棋子
            if pos in RIVER:
                pos = (self._pos[0]+(pos[0]-self._pos[0])*3,
                       self._pos[1]+(pos[1]-self._pos[1])*4)
                if not self.river_passable(pos, board):
                    return 0
            if pos not in board.all_pos()[self.team] and 0 <= pos[0] <= 6 and 0 <= pos[1] <= 8 and pos != HOME[self.team]:
                if not(pos in board.all_pos()[not self.team] and self.compare_value(board.piece_on(pos)) == self):
                    self._passable_area.append(pos)

        get(self._pos[0], self._pos[1]+1)
        get(self._pos[0], self._pos[1]-1)
        get(self._pos[0]+1, self._pos[1])
        get(self._pos[0]-1, self._pos[1])
        return self._passable_area


class Mouse(Piece):
    def __init__(self, name, team, *pos):
        super(Mouse, self).__init__(name, team, *pos)

    def get_passable_area(self, board):
        """ 获取能移动的位置 """
        self._passable_area = []  # 重置target_area
        #print("获取可移动位置时的poslist：\n", self.board[self.team].keys())

        def get(*pos: tuple):
            if not(pos in board.all_pos()[not self.team] and self.compare_value(board.piece_on(pos)) == self):
                if self._pos not in RIVER:
                    # 避开己方棋子
                    if pos not in board.all_pos()[self.team] and 0 <= pos[0] <= 6 and 0 <= pos[1] <= 8 and pos != HOME[self.team]:
                        self._passable_area.append(pos)
                else:
                    if pos not in board.all_pos()[self.team] and pos not in board.all_pos()[not self.team]:
                        self._passable_area.append(pos)

        get(self._pos[0], self._pos[1]+1)
        get(self._pos[0], self._pos[1]-1)
        get(self._pos[0]+1, self._pos[1])
        get(self._pos[0]-1, self._pos[1])
        return self._passable_area


class PieceSprite(pygame.sprite.Sprite):
    """ 渲染棋子 """
    def __init__(self, group, piece: Piece, board):

        super().__init__(group)

        self.piece = piece
        self.board = board
        self._image = pygame.Surface((48, 48))
        

    @property
    def real_pos(self):
        """ 棋子在窗口中的的实际坐标 """
        return (self.piece.pos[0]*50+1, self.piece.pos[1]*50+1)

    @property
    def rect(self):
        return self._image.get_rect(topleft=self.real_pos)

    @property
    def back_color(self):
        """ 根据是否在河中切换背景色 """
        if self.piece.pos in RIVER:
            self._back_color = 'deepskyblue'
        else:
            self._back_color = 'white'
        return self._back_color

    @property
    def image(self):
        """ 图像 """
        self._image.fill(self.back_color)
        self._font_surface = font.render(
            self.piece.name, True, TEAM[self.piece.team], self.back_color)
        self._image.blit(self._font_surface, (10, 4))
        if self.piece.choosen:
            pygame.draw.rect(self._image, "gold", (0, 0, 48, 48), 3)
        return self._image

    def remove_from_group(self):
        if self.piece.pos not in self.board.all_pos()[self.piece.team]:
            self.kill()


    def update(self):
        self.remove_from_group()


if __name__ == "__main__":
    pass
