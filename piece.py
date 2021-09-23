""" 棋子类
棋子的选中、移动、吃子的判断将在这里被完成，会向外界留一个move的接口，通过传入的pos来操控棋子"""
#TODO 目前该模块已经实现通过传入坐标实现棋子移动、吃子的方法，还需完成棋子的选中与取消和狮虎、老鼠两个子类的移动位置的方法重写,棋子的形象绘制

import pygame

pygame.init()

font = pygame.font.Font('msyh.ttf', 30)


animal = ["鼠","猫","狗","狼","豹","虎","狮","象"]

RIVER:tuple = ((1,3),(1,4),(1,5),(2,3),(2,4),(2,5),(4,3),(4,4),(4,5),(5,3),(5,4),(5,5)) #储存的代表河水的坐标

TEAM = ("black","red")  


class Piece(object):

    pos_list = {TEAM[0]:{},TEAM[1]:{}}  #储存该类所有对象和其位置，棋子通过change_pos方法改变坐标时会同步到此处
    turn = False #默认黑队
    piece_picked = [0] #储存被选中的piece对象

    def mousepos_to_cr(mouse_pos):
        """ 用于将鼠标点击传入坐标与棋子行列数的换算 """
        print(mouse_pos)
        return mouse_pos[0]//50,mouse_pos[1]//50



    def __init__(self,name,team:int,*pos):
        self._pos = pos #pos为行列数,左上角为0,0

        self.team = TEAM[team]  #team传入0或1

        self.name = name

        self.value = animal.index(self.name)

        self.text = font.render(self.name, True, pygame.Color(self.team), (255,255,255))
        
        self.pos_list[self.team][self]=self._pos    #TODO这里使用列表让成员来修改类变量，我不知道是否合适；这样的用法还出现在piece_picked这一类变量中。
        
        self.target_area = []   #储存棋子能走的坐标的列表，用get_target_area方法初始化和更新
        self.get_target_area()  
    
    def get_pos(self):
        return self._pos

    def get_real_pos(self):
        """ 获取棋子的实际坐标 """
        return (self._pos[0]*50,self._pos[1]*50)

    def change_pos(self,pos):
        """ 更改self._pos，将其同步至slef.pos_list，同时更新target_area """
        self._pos = pos
        self.pos_list[self.team][self]=self._pos
        self.get_target_area()

    def picked_me(self):
        self.piece_picked[0]=self
    
    def not_picked(self):   
        self.piece_picked[0] = 0

    def get_target_area(self):
        """ 获取能移动的位置 """
        #TODO狮虎和老鼠类继承时将重写它
        self.target_area = []   #重置target_area
        def get(*pos:tuple):
            if pos not in RIVER and pos not in self.pos_list[self.team].values():   #避开河流和己方棋子
                self.target_area.append(pos)

        get(self._pos[0], self._pos[1]+1)
        get(self._pos[0], self._pos[1]-1)
        get(self._pos[0]+1, self._pos[1])
        get(self._pos[0]-1, self._pos[1])


    def del_me(self):
        """ 被吃时移除棋子的方法 """
        self.change_pos((-1,-1))


    def eat(self,other):
        """ 两棋子相遇时执行吃子的判断 """

        if other.value > self.value:
            print("我被吃了")
            self.del_me()

        elif other.value <= self.value:
            print("{}队的{}被吃了".format(other.team,other.name))
            other.del_me() 


    def move(self,pos):
        """ 传入坐标后移动棋子，并完成吃子等相应判断 """
        print("{}要往{}走了".format(self.name,pos))
        self.change_pos(pos)

        #获取敌人的队伍enemy_team，很别扭
        a=list(TEAM)
        a.remove(self.team)
        enemy_team = a[0]
        print("enemy team is {}".format(enemy_team))

        if pos in tuple(self.pos_list[enemy_team].values()):    #判断：如果棋子与敌方的棋子相遇
            self.eat([k for k,v in self.pos_list[enemy_team].items() if v == pos].pop())    #通过值找到储存敌方棋子的对象的键

    @classmethod
    def get_all_pieces(cls):
        """ 返回包含所有棋子的元组 """
        return tuple(cls.pos_list[TEAM[0]].keys())+tuple(cls.pos_list[TEAM[1]].keys())

    @classmethod
    def get_piece_picked(cls):
        """ 返回被选中的棋子对象 
            返回0时表示无选中棋子
            """
        print(cls.piece_picked)
        return cls.piece_picked[0]

    @classmethod
    def reponse_click(cls,pos):
        """ 响应鼠标在棋盘内的点击
        pos : 行列数
         """
        print("点击位置为{}".format(pos))
        #TODO：打算通过直接使用类的类函数来响应，这样是否是可行的?(piece_picked能否被修改)这样是否是恰当的?
        if cls.get_piece_picked() == 0:
            if pos in tuple(cls.pos_list[TEAM[cls.turn]].values()):             
                [k for k,v in cls.pos_list[TEAM[cls.turn]].items() if v == pos].pop().picked_me()    #选中行动方的棋子

        else:
            if pos in cls.get_piece_picked().target_area: #点击坐标在传入棋子的可行动范围内，移动棋子，轮换执棋 
                cls.get_piece_picked().move(pos)
                print("我的坐标是",cls.get_piece_picked()._pos)
                cls.get_piece_picked().not_picked()
                cls.turn = not cls.turn
                print("轮到",TEAM[cls.turn])
            elif pos == cls.get_piece_picked()._pos:  #点击正选中的棋子，取消选中
                cls.get_piece_picked().not_picked()
            elif pos in tuple(cls.pos_list[TEAM[cls.turn]].values()):  #选中己方其他棋子，选中该棋子
                cls.get_piece_picked().not_picked()
                [k for k,v in cls.pos_list[TEAM[cls.turn]].items() if v == pos].pop().picked_me() 
            else:
                cls.get_piece_picked().not_picked()   #其他情况，取消选中

            




  


if __name__ == "__main__":
    cat = Piece("猫",0,1,2)
    print(cat.pos_list)

    dog = Piece("狗",1,1,3)
    print(dog.pos_list)
    dog.get_target_area()
    print(dog.target_area)
    dog.move(1,2)
    print(dog._pos)
    print(dog.pos_list)
    cat.picked_me()
    print(Piece.piece_picked)



        