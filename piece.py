""" 棋子类 """

import pygame
pygame.init()
font = pygame.font.Font('msyh.ttf', 30)

animal = ["鼠","猫","狗","狼","豹","虎","狮","象"]


class Piece():
    def __init__(self,name,team,*pos):
        self.pos = list(pos) #pos为行列数,左上角为0,0
        self.team = team
        self.onchoise = False
        self.name = name
        self.value = animal.index(self.name)
        self.actual_pos = (self.pos[0]*50+9,self.pos[1]*50+5) #棋子坐标
        self.text = font.render(self.name, True, self.team, (0,133,133))

    def move(self,goal_pos):
        pos_before_move = tuple(self.pos)
        print(pos_before_move)
        #移动到相邻格子
        if goal_pos[0]//50 == self.pos[0] and abs(self.pos[1]-goal_pos[1]//50)==1:
            self.pos[1]=goal_pos[1]//50
        if goal_pos[1]//50 == self.pos[1] and abs(self.pos[0]-goal_pos[0]//50)==1:
            self.pos[0]=goal_pos[0]//50
        self.actual_pos = (self.pos[0]*50+9,self.pos[1]*50+5)
        print(self.pos)
        print(pos_before_move)
        if pos_before_move == tuple(self.pos):#没有移动
            return 0
        elif pos_before_move != tuple(self.pos):
            return 1

    def choise(self,pos):
        if pos[0]//50==self.pos[0] and pos[1]//50==self.pos[1]:
            self.onchoise = not self.onchoise
        



    def del_me(self):
        self.pos = [-1,-1]
        self.actual_pos = (self.pos[0]*50,self.pos[1]*50)

    def eat(self,other):
        if other.pos == self.pos:
            if other.value > self.value:
                print("我被吃了")
                self.del_me()
            elif other.value <= self.value:
                print("ohter被吃了")
                other.del_me()   
            else:
                self.del_me()
                other.del_me()  

    def across_river(self):
        pass






        