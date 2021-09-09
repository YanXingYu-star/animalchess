import pygame  # 引入
import sys
# import pygame.freetype  #为在窗口显示字符引入freetype
from math import pi
import piece

# pygame初始化
pygame.init()
screen = pygame.display.set_mode((50*7+200, 50*9))
pygame.display.set_caption("斗兽棋")
clock = pygame.time.Clock()

font = pygame.font.Font('msyh.ttf', 30)

RED = pygame.Color('red')
GOLD = 255, 251, 0
BLACK = 0, 0, 0  # 窗口颜色的R  值
BLUE = 0,0,255
GREEN = 0,255,0
WHITE = 255,255,255
animal = ["鼠","猫","狗","狼","豹","虎","狮","象"]
turn = False #此时蓝队执棋

#创建两个队伍的棋子，放在队伍列表里
red = []
blue=[]
for i in range(7):
    red.append(piece.Piece(animal[i], RED,i,0))
for j in range(7):
    blue.append(piece.Piece(animal[j], BLUE,j,8))



#存队伍中棋子的位置，避免同队棋子重合
pos_red=[]
pos_blue=[]
for i in range(7):
    pos_red.append(red[i].pos)
for i in range(7):
    pos_blue.append(blue[i].pos)

#主循环
while True:
    clock_time = clock.tick_busy_loop(60)    
    screen.fill(WHITE) 
    if not turn:
        tt = font.render("该红方了", True, RED,(255,255,255))
    else:
        tt = font.render("该蓝方了", True, BLUE,(255,255,255))
    screen.blit(tt,[390,200])
    #画格子
    for x in range(7):
        for y in range(9):
            pygame.draw.rect(screen, BLACK, (x*50, y*50, 50, 50), 1)  
    
    #画河
    for y in range(3,6):
        for x in (1,2,4,5):
            pygame.draw.rect(screen, BLUE, (x*50, y*50, 50, 50), 0) #0即填充            
    #选择棋子的框
    for i in range(7):
        if red[i].onchoise:
            pygame.draw.rect(screen,GOLD,(red[i].pos[0]*50,red[i].pos[1]*50,50,50),1)
        if blue[i].onchoise:
            pygame.draw.rect(screen,GOLD,(blue[i].pos[0]*50,blue[i].pos[1]*50,50,50),1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #点击事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                choose_pos = [event.pos[0]//50,event.pos[1]//50]
                if not turn:
                    for i in range (7):
                        if red[i].onchoise:
                            if choose_pos not in pos_red:#防止与同队棋子重合
                                a=red[i].move(event.pos)
                                if a:
                                    turn = not turn
                                print(a,turn)
                                #red[i].onchoise=False
                                red[i].choise(event.pos)#取消选中
                                for j in range(7):
                                    red[i].eat(blue[j])
                            else:
                                red[i].onchoise=False
                        elif not red[i].onchoise:
                            red[i].choise(event.pos)
                    event.pos = (-1,-1)
                    #print(choose_pos,red[0].pos,red[1].pos)
                else:
                    for i in range(7):
                        if blue[i].onchoise:
                            if choose_pos not in pos_blue:
                                a = blue[i].move(event.pos)
                                if a:
                                    turn = not turn
                                #print(a,turn)
                                blue[i].choise(event.pos)
                                for j in range(7):
                                    blue[i].eat(red[j])
                            else:
                                blue[i].onchoise=False
                        elif not blue[i].onchoise:
                            blue[i].choise(event.pos)
                    event.pos = (-1,-1)

    for i in range(7):
        screen.blit(red[i].text,red[i].actual_pos)
        screen.blit(blue[i].text,blue[i].actual_pos)

    pygame.display.update()     #刷新屏幕