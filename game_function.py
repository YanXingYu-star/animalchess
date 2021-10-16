import pygame
import piece
import sys
import json

pygame.init()
screen = pygame.display.set_mode((50*7+200, 50*9))
pygame.display.set_caption("斗兽棋")
clock = pygame.time.Clock()

WHITE = 255,255,255

def limit_frame():
    """ 限制帧数 """
    clock_time = clock.tick_busy_loop(60) 

def create_piece():
    with open("piece.json", "r",encoding="utf-8") as f:
        data = json.load(f)    
    for i in data['piece']:
        piece.Piece(i["name"],i["team"],*eval(i["pos"]))

def draw_river():
    for pos in piece.RIVER:
        pygame.draw.rect(screen, (0,0,255), (pos[0]*50, pos[1]*50, 50, 50), 0) 

def draw_checkerboard():
    """ 绘制棋盘 """
    for x in range(7):
        for y in range(9):
            pygame.draw.rect(screen, (0,0,0), (x*50, y*50, 50, 50), 1) 
    draw_river()


def _reponse_click(pos):
    """ 响应鼠标点击，负责棋子的选中、取消和移动 """
    piece.Piece.reponse_click(pos)


def event_check():

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                _reponse_click(piece.Piece.mousepos_to_cr(event.pos))

def draw_choice():
    """ 画选中棋子的金框 """
    if piece.Piece.get_piece_picked() != 0:
        pos = piece.Piece.get_piece_picked().get_real_pos()
        pygame.draw.rect(screen, (255,251,0), (pos[0], pos[1], 50, 50), 3) 


def blit_screen():
    screen.fill(WHITE) 
    draw_checkerboard()
    for a_piece in piece.Piece.get_all_pieces():    #依次绘制各棋子
        screen.blit(a_piece.text, a_piece.get_real_pos())
    draw_choice()
    pygame.display.update()

if __name__ == '__main__':
    create_piece()
    print(piece.Piece.get_all_pieces())