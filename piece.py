""" 该模块包含Piece类和其两个子类"""
from typing import List, Dict, Tuple
from settings import *
import pygame

class Piece(pygame.sprite.Sprite):
    """ Piece类
        实例具有移动位置，判断吃子等方法.
        包含几个批量的控制棋子的类的方法，以及控制吃子的方法 """

    @classmethod
    def reset(cls):
        """ 初始化类变量 """
        cls.pos_list = [{}, {}]
        cls.piece_picked = [None]  # 储存被选中的Piece对象
        cls.game_over = [None]
        cls.turn = [0]
        cls.click_pos = [None]
        cls.reponse_num = 0

    def __init__(self,group, name, team: bool, *pos):

        super().__init__(group)

        self._pos = pos  # pos为行列数,左上角为0,0
        self.team = team  # team传入0或1
        self.name = name
        self._value = animal.index(self.name)+1  # 用ANIMAL列表中的顺序来代表棋子的价值，用来判断吃子
        self.pos_list[self.team][self.pos] = self

        # 图形
        self._image = pygame.Surface((49,49))
        self.rect = self._image.get_rect(topleft=self.real_pos)
        self._font_surface = font.render(self.name, True, TEAM[self.team],'white')
        
    
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        """ 将self._pos更新至cls.board """

        self.pos_list[self.team].pop(self.pos,0) 
        self._pos = pos
        self.pos_list[self.team][self.pos] = self
        self.rect = self.image.get_rect(topleft=self.real_pos)

        self.pos_list[not self.team].pop(self.pos,1)

        if self.pos == HOME[not self.team]:
            self.game_over[0] = True
        if not self.all_pos()[not self.team]:
            self.game_over[0] = True

        return self.pos

    @property
    def real_pos(self):
        """ 获取棋子的实际坐标 """
        return (self.pos[0]*50, self.pos[1]*50)

    @property
    def blit_pos(self):
        """ 获得棋子偏移后的实际坐标 """
        return (self.pos[0]*50 + DETA_X+20, self.pos[1]*50 + DETA_Y+20)

    @property
    def value(self):
        if self.pos in TRAP[not self.team]:  # 敌方陷阱中的棋子价值为0
            return 0
        else:
            return self._value

    @property
    def image(self):
        self._image.fill("white")
        self._image.blit(self._font_surface,(10,4))
        if self.piece_picked[0] == self:
            pygame.draw.rect(self._image,GOLD, (0, 0,50, 50), 2)
        return self._image


    def input(self,pos):
        """ 棋子响应传入坐标 """
        if pos:
            if self.turn[0] == self.team:
                print("is turn")
                #被选中
                if self.piece_picked[0] == self:
                    if pos in self.passable_area:
                        self.pos = pos
                        self.piece_picked[0] = None
                        self.turn[0] = not self.turn[0]
                        print("move",self.name,self.team,self.pos)
                    else:
                        self.piece_picked[0] = None
                        print("cancel",self.name,self.team)
                    self.click_pos[0] = None
                    
                else:
                    print(pos,self.pos)
                    if pos == self.pos:
                        self.click_pos[0] = None
                        self.piece_picked[0] = self
                        print(self.piece_picked[0],self.name,self.team)
                        print("choose",self.name,self.team)

    def remove_from_group(self):
        if self.pos not in self.all_pos()[self.team]:
            self.kill()
            print("kill",self.name,self.team)
              
    def update(self):
        self.input(self.click_pos[0])
        self.remove_from_group()
    
    def compare_value(self, target_piece: 'Piece'):
        """ 比较两棋子的价值，返回价值较小的棋子 """

        # 陷阱中的棋子被吃
        if target_piece.value == 0:  
            print("is 1")
            return target_piece
        # 老鼠吃大象
        elif self.value == 1 and target_piece.value == 8:
            print("is 2")
            return target_piece
        elif self.value == 8 and target_piece.value == 1:
            print("is 3")
            return self
        # 大吃小
        elif self.value >= target_piece.value:
            print("is 4")
            return target_piece
        elif self.value < target_piece.value:
            print("is 5")
            return self

    @property
    def passable_area(self):
        """ 输出包含可移动的位置的列表"""
        self._passable_area = []  # 重置target_area

        def get(*pos: tuple):
            # 避开河流和己方棋子
            if pos not in RIVER and pos not in self.all_pos()[self.team] and 0 <= pos[0] <= 6 and 0 <= pos[1] <= 8:
                if not(pos in self.all_pos()[not self.team] and self.compare_value(self.piece_on(pos)) == self):

                    self._passable_area.append(pos)

        get(self._pos[0], self._pos[1]+1)
        get(self._pos[0], self._pos[1]-1)
        get(self._pos[0]+1, self._pos[1])
        get(self._pos[0]-1, self._pos[1])

        return self._passable_area



    @classmethod
    def all_pos(cls):
        """ 返回指定队伍棋子的坐标 """
        team0_pos = list(cls.pos_list[0].keys())
        team1_pos = list(cls.pos_list[1].keys())
        return team0_pos, team1_pos, team0_pos+team1_pos

    @classmethod
    def all_piece(cls) -> Tuple[List['Piece']]:
        """ 返回包含所有棋子的元组 """
        team0_pieces = list(cls.pos_list[0].values())
        team1_pieces = list(cls.pos_list[1].values())
        return team0_pieces, team1_pieces, team0_pieces+team1_pieces

    @classmethod
    def piece_on(cls, pos) -> 'Piece':
        """ 通过传入坐标返回棋子对象 """
        if pos in cls.all_pos()[0]:
            return cls.pos_list[0][pos]
        elif pos in cls.all_pos()[1]:
            return cls.pos_list[1][pos]
        else:
            return None



    @classmethod
    def get_next_steps(cls, turn) -> List[tuple]:
        """ 获取可走的下一步棋 """
        next_steps = []
        for piece in cls.all_piece()[turn]:
            next_steps += map(lambda pos: (piece.pos, pos),
                              piece.passable_area)
        return next_steps

    @classmethod
    def get_piece_picked(cls) -> 'Piece':
        """ 返回被选中的棋子对象 
            返回0时表示无选中棋子
            """
        return cls.piece_picked

    @classmethod
    def set_piece_picked(cls, piece: 'Piece'):
        cls.piece_picked = piece

    @classmethod
    def clear_piece_picked(cls):
        cls.piece_picked = None



    @staticmethod
    def convert_to_board(window_pos):
        """ 将窗口坐标转换为棋盘坐标 """
        #print(window_pos)
        return window_pos[0]//50, window_pos[1]//50

    @classmethod
    def get_board_matrix(cls):
        board_matrix = [[None]*BOARD_COLUMN for i in range(BOARD_ROW)]
        for row in range(BOARD_COLUMN):
            for column in range(BOARD_ROW):
                pos = (row,column)
                if cls.piece_on(pos):
                    board_matrix[row][column] = cls.piece_on(pos).value
                else:
                    board_matrix[row][column] = 0

        return board_matrix


class LionTiger(Piece):

    def __init__(self, name, team, *pos):
        super(LionTiger, self).__init__(name, team, *pos)

    @property
    def passable_area(self):
        """ 获取能移动的位置 """
        self._passable_area = []  # 重置target_area

        def get(*pos: tuple):
            # 避开己方棋子
            if pos in RIVER:
                pos = (self._pos[0]+(pos[0]-self._pos[0])*3, self._pos[1]+(pos[1]-self._pos[1])*4)
            if pos not in self.all_pos()[self.team] and 0 <= pos[0] <= 6 and 0 <= pos[1] <= 8:
                if not(pos in self.all_pos()[not self.team] and self.compare_value(self.piece_on(pos)) == self):
                    self._passable_area.append(pos)

        get(self._pos[0], self._pos[1]+1)
        get(self._pos[0], self._pos[1]-1)
        get(self._pos[0]+1, self._pos[1])
        get(self._pos[0]-1, self._pos[1])
        return self._passable_area


class Mouse(Piece):
    def __init__(self, name, team, *pos):
        super(Mouse, self).__init__(name, team, *pos)
    
    @property
    def back_color(self):
        if self.pos in RIVER:
            self._back_color = 'blue'
        else:
            self._back_color = 'white'
        return self._back_color

    @property
    def image(self):
        self._image.fill(self.back_color)
        self._font_surface = font.render(self.name, True, TEAM[self.team],self.back_color)
        self._image.blit(self._font_surface,(10,4))
        if self.piece_picked[0] == self:
            pygame.draw.rect(self._image,GOLD, (0, 0,50, 50), 2)
        return self._image

    @property
    def passable_area(self):
        """ 获取能移动的位置 """
        self._passable_area = []  # 重置target_area
        #print("获取可移动位置时的poslist：\n", self.board[self.team].keys())

        def get(*pos: tuple):
            if not(pos in self.all_pos()[not self.team] and self.compare_value(self.piece_on(pos)) == self):
                if self._pos not in RIVER:
                    # 避开己方棋子
                    if pos not in self.all_pos()[self.team] and 0 <= pos[0] <= 6 and 0 <= pos[1] <= 8:
                        self._passable_area.append(pos)
                else:
                    if pos not in self.all_pos()[self.team] and pos not in self.all_pos()[not self.team]:
                        self._passable_area.append(pos)

        get(self._pos[0], self._pos[1]+1)
        get(self._pos[0], self._pos[1]-1)
        get(self._pos[0]+1, self._pos[1])
        get(self._pos[0]-1, self._pos[1])
        return self._passable_area


if __name__ == "__main__":
    pass
