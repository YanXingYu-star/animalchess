""" 该模块包含Piece类和其两个子类"""

from typing import List,Dict
from setting import *

class Piece(object):
    """ Piece类
        实例具有移动位置，判断吃子等方法.
        包含几个批量的控制棋子的类的方法，以及控制吃子的方法 """
    
    board = [{},{}]
    turn = 0  # 两个队伍的轮换，0为黑队
    piece_picked = [0]  # 储存被选中的Piece对象
    game_over = [1]  



    def __init__(self, name, team: bool, *pos):
        self._pos = pos  # pos为行列数,左上角为0,0
        self.team = team  # team传入0或1
        self.name = name
        self._value = animal.index(self.name)  # 用ANIMAL列表中的顺序来代表棋子的价值，用来判断吃子       
        self.board[self.team][self._pos] = self
        
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        """ 将self._pos更新至cls.board """
        del self.board[self.team][self._pos]
        self._pos = pos
        self.board[self.team][self._pos] = self
        return self.pos

    @property
    def real_pos(self):
        """ 获取棋子的实际坐标 """
        return (self.pos[0]*50, self.pos[1]*50)

    @property
    def blit_pos(self):
        """ 获得棋子便宜后的实际坐标 """
        return (self.pos[0]*50 + DETA_X, self.pos[1]*50 + DETA_Y)
    
    @property
    def value(self):
        if self.pos in TRAP[not self.team]: #敌方陷阱中的棋子价值为-1
            return -1
        else:
            return self._value


    @property
    def passable_area(self):
        """ 输出包含可移动的位置的列表"""
        self._passable_area = []  # 重置target_area

        def get(*pos: tuple):
            # 避开河流和己方棋子
            if pos not in RIVER and pos not in self.board[self.team].keys():

                self._passable_area.append(pos)

        get(self._pos[0], self._pos[1]+1)
        get(self._pos[0], self._pos[1]-1)
        get(self._pos[0]+1, self._pos[1])
        get(self._pos[0]-1, self._pos[1])

        return self._passable_area

    

    def picked_me(self):
        self.piece_picked[0] = self

    def not_picked(self):
        self.piece_picked[0] = 0



    def del_me(self):
        """ 移除棋子的方法 """
        self.pos = (-1, -1)

        for pos in self.board[self.team].keys():
            #判断己方有无棋子存活
            if pos != (-1, -1):
                break
        else:
            self.game_over.append(1)

    def compare_value(self,target_piece:'Piece'):
        """ 两棋子相遇时进行价值判断，返回较小的棋子 """
        print(self.value)
        print(target_piece.value)
        #该方法默认self为主动的棋子
        #吃掉陷阱中的棋子
        if target_piece.value == -1:
            print("is 1")
            return target_piece
        #老鼠吃大象
        elif self.value == 0 and target_piece.value == 7:
            print("is 2")
            return target_piece
        elif self.value == 7 and target_piece.value == 0:
            print("is 3")
            return self
        #大吃小
        elif self.value >= target_piece.value:
            print("is 4")
            return target_piece
        elif self.value < target_piece.value:
            print("is 5")
            return self

    def move(self, pos):
        """ 传入坐标后移动棋子，并完成吃子等相应判断 """
        self.pos = pos

        # 判断：如果棋子与敌方的棋子相遇
        if pos in self.all_pos(not self.team):

            self.compare_value(self.board[not self.team][pos]).del_me()
        print('is here')
        if pos in (HOME[not self.team], 1):
            self.game_over.append(1)
            print("Game Over")

    @classmethod
    def all_piece(cls,team='all') -> List['Piece']:
        """ 返回包含所有棋子的元组 """
        if team == 'all':
            return tuple(cls.board[0].values())+tuple(cls.board[1].values())
        else:
            return tuple(cls.board[team].values())

    @classmethod
    def all_pos(cls,team='all'):
        """ 返回指定队伍棋子的坐标 """
        if team == 'all':
            return tuple(cls.board[0].keys())+tuple(cls.board[1].keys())
        else:
            return tuple(cls.board[team].keys())

    @classmethod
    def piece_picked_1(cls):
        pass

    @classmethod
    def get_piece_picked(cls) -> 'Piece': 
        """ 返回被选中的棋子对象 
            返回0时表示无选中棋子
            """
        return cls.piece_picked[0]

    @classmethod
    def reboot(cls):

        cls.board = [{},{}]
        cls.turn = False  # 两个队伍的轮换，false为黑队
        cls.piece_picked = [0]  # 储存被选中的Piece对象
        cls.game_over = []  # 空列表表示None

    @staticmethod
    def convert_to_board(window_pos):
        """ 将窗口坐标转换为棋盘坐标 """
        print(window_pos)
        return window_pos[0]//50, window_pos[1]//50


class Lion_tiger(Piece):

    def __init__(self, name, team, *pos):
        super(Lion_tiger, self).__init__(name, team, *pos)

    @property
    def passable_area(self):
        """ 获取能移动的位置 """
        self._passable_area = []  # 重置target_area

        def get(*pos: tuple):
            if pos not in self.board[self.team].keys():  # 避开己方棋子
                if pos in RIVER:
                    self._passable_area.append(
                        (self._pos[0]+(pos[0]-self._pos[0])*3, self._pos[1]+(pos[1]-self._pos[1])*4))
                else:
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
    def passable_area(self):
        """ 获取能移动的位置 """
        self._passable_area = []  # 重置target_area
        print("获取可移动位置时的poslist：\n", self.board[self.team].keys())

        def get(*pos: tuple):
            if self._pos not in RIVER:
                if pos not in self.board[self.team].keys():  # 避开己方棋子
                    self._passable_area.append(pos)
            else:
                if pos not in self.board[0].keys() and pos not in self.board[1].keys():
                    self._passable_area.append(pos)


        get(self._pos[0], self._pos[1]+1)
        get(self._pos[0], self._pos[1]-1)
        get(self._pos[0]+1, self._pos[1])
        get(self._pos[0]-1, self._pos[1])
        return self._passable_area

if __name__ == "__main__":
    Piece.board[0]["test"]=30
    print(Piece.board)
    dog = Piece("狗", 0, 3, 1)
    print(dog.board)
    dog.passable_area
    print(dog.passable_area)
    dog.move((3, 0))
    print(dog._pos)
    print(dog.board)
    print(dog.game_over)
