import function_in_game as fun
import screen_setting as sset
import start_menu


fun.create_piece()


def start_check_click(pos):
        print(start_menu.start_button.check_click(pos))
        print("open:{}".format(start_menu.start_button.open))


while True:
    """ 开始界面 """
    start_menu.blit_start_screen()
    sset.event_check(start_check_click)

    while start_menu.game_start.take_effect:
        """ 进入对局 """
        if fun.is_game_over():
            fun.blit_game_over()
            start_menu.game_start.toggle_switch()
            fun.create_piece()

        sset.event_check(fun.reponse_click)
        fun.blit_game_screen()

