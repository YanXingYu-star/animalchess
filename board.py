import pygame
from settings import *

font = pygame.font.Font(FONT, 30)

class Board(pygame.sprite.Sprite):
    def __init__(self,group,width,height):
        super().__init__(group)
        self.width = width
        self.height = height

        self.image = pygame.Surface((width*50,height*50))
        self.rect = self.image.get_rect()
        self.draw_board()

    def draw_board(self):
        """ 绘制棋盘 """

        self.image.fill('white')

        #画格子
        for x in range(self.width):
            for y in range(self.height):
                pygame.draw.rect(self.image,"black", (x*50, y*50, 50, 50), 1)

        #河流
        for pos in RIVER:
            pygame.draw.rect(self.image,"deepskyblue",(pos[0]*50, pos[1]*50,50,50),0)
        #陷阱
        for t in TRAP:
            for pos in t:       
                trap_surface=font.render("陷",True,"blue","white")
                self.image.blit(trap_surface,(pos[0]*50+DETA_X, pos[1]*50+ DETA_Y))

        #兽穴
        for pos in HOME:
            home_surface = font.render("穴",True,"blue","white")
            self.image.blit(home_surface,(pos[0]*50+ DETA_X, pos[1]*50+ DETA_Y))
    
    def update(self):
        pass