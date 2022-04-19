import pygame
import sys
pygame.init()

font = pygame.font.Font('msyh.ttf', 30)

class Switch(object):
    def __init__(self):
        self.take_effect = False

    def toggle_switch(self):
        self.take_effect = not self.take_effect
            
class Button(object):
    def __init__(self,rect,text,switch=None):
        self.rect=pygame.Rect(rect)    #按键的矩形(left,top,width,height) 
        self.text = font.render(text, True, (0,0,0), (255,255,255))     #
        self.status = 1     #1：按钮可以按
        self.open = 0   #1：按钮开启 0：按钮关闭
        self.switch:Switch = switch
    
    def open_me(self):
        self.open = not self.open
        if self.switch != None:
            self.switch.toggle_switch()

    def is_click(self,click_pos):
        if self.status == 0:
            return False
        else:
            if self.rect.collidepoint(click_pos):   #判断pos是否在self.rect内
                self.open_me()
            return self.rect.collidepoint(click_pos)

    def check_click(self,pos):

            return self.is_click(pos)

    def blit_parameter(self):
        """ 返回pygame.blit所需的一些参数 """
        return (self.text,self.rect)

game_start = Switch()
start_button = Button((400,50,100,50),"开始游戏",game_start)

game_pause = Switch()
pause_button = Button((400,150,100,50),"暂停游戏",game_pause)

if __name__ == "__main__":
    screen = pygame.display.set_mode((50*7+200, 50*9))
    while True:
        screen.blit(start_button.text, start_button.rect)
        pygame.display.update()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    print(start_button.check_click(event.pos))
                    print("open:{}".format(start_button.open))