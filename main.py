import function_in_game as fun
import screen_setting as sset
import start_interface
import piece

fun.create_piece()


def start_check_click(pos):
        print(start_interface.start_button.check_click(pos))
        print("open:{}".format(start_interface.start_button.open))


while True:
    """ 开始界面 """
    sset.blit_start_screen()
    sset.event_check(start_check_click)

    while start_interface.game_start.take_effect:
        """ 进入对局 """
        if piece.Piece.game_over:
            sset.blit_game_over()
            start_interface.game_start.toggle_switch()
            fun.create_piece()

        fun.draw_checkerboard()
        sset.event_check(fun.reponse_click)

        sset.blit_game_screen()

