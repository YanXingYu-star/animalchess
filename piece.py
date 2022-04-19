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
        self.value = animal.index(self.name)  # 用ANIMAL列表中的顺序来代表棋子的价值，用来判断吃子       
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


    def eat_in_trap(self, other):
        other.del_me()

    def eat(self, other):
        """ 两棋子相遇时执行吃子的判断 """
        # value之差和7进行判断是为了让老鼠吃大象，感觉有点绕

        if other.value-self.value == 7 or other.value <= self.value and self.value-other.value != 7:
            print("{}队的{}被吃了".format(other.team, other.name))
            other.del_me()
        elif other.value > self.value or self.value-other.value == 7:
            print("我被吃了")
            self.del_me()


    def move(self, pos):
        """ 传入坐标后移动棋子，并完成吃子等相应判断 """
        self.pos = pos
        if pos in TRAP[self.team] and pos in tuple(self.board[not self.team].keys()):
            print("in trap")
            self.eat_in_trap(self.board[not self.team][pos])
        else:
            # 判断：如果棋子与敌方的棋子相遇
            if pos in tuple(self.board[not self.team].keys()):
                # 通过值找到储存敌方棋子的对象的键
                self.eat(self.board[not self.team][pos])
            print('is here')
            if pos in (HOME[not self.team], 1):
                self.game_over.append(1)
                print("Game Over")

    @classmethod
    def all_piece(cls,team='all'):
        """ 返回包含所有棋子的元组 """
        if team == 'all':
            return tuple(cls.board[0].values())+tuple(cls.board[1].values())
        else:
            return tuple(cls.board[team].values())

    @classmethod
    def all_pos(cls,team='all'):
        if team == 'all':
            return tuple(cls.board[0].keys())+tuple(cls.board[1].keys())
        else:
            return tuple(cls.board[team].keys())

    @classmethod
    def get_piece_picked(cls):
        """ 返回被选中的棋子对象 
            返回0时表示无选中棋子
            """

        return cls.piece_picked[0]

    @classmethod
    def reponse_click(cls, pos):
        """ 响应鼠标在棋盘内的点击
        pos : 行列数
         """
        print("点击位置为{}".format(pos))

        if cls.get_piece_picked() == 0:
            if pos in tuple(cls.board[cls.turn].keys()):
                cls.board[cls.turn][pos].picked_me()
                print("被选中的棋子是"+cls.get_piece_picked().name)
                print("它可走的位置是", cls.get_piece_picked().passable_area)
        else:

            if pos in cls.get_piece_picked().passable_area:  # 点击坐标在传入棋子的可行动范围内，移动棋子，轮换执棋
                cls.get_piece_picked().move(pos)
                cls.get_piece_picked().not_picked()
                cls.turn = not cls.turn

            elif pos == cls.get_piece_picked()._pos:  # 点击正选中的棋子，取消选中
                cls.get_piece_picked().not_picked()
            # 选中己方其他棋子，选中该棋子
            elif pos in tuple(cls.board[cls.turn].keys()):
                cls.get_piece_picked().not_picked()
                cls.board[cls.turn][pos].picked_me()


            else:
                cls.get_piece_picked().not_picked()  # 其他情况，取消选中

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
