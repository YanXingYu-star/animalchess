import game_function as gf


gf.create_piece()
print(1)


while True:
    gf.draw_checkerboard()
    gf.event_check()
    
    gf.blit_screen()