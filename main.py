import function_in_game as fun
import menu



fun.create_piece()

while True:
    """ 开始界面 """
    menu.blit_start_screen()
    menu.start_check_click()

    while menu.game_start.take_effect:
        """ 进入对局 """
        if fun.is_game_over():
            fun.blit_game_over()
            menu.game_start.toggle_switch()
            fun.create_piece()

        fun.reponse_click()
        fun.blit_game_screen()

