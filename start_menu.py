"""该模块用于构建开始菜单 """
import screen_setting

class Switch(object):
    def __init__(self):
        self.take_effect = False

    def toggle_switch(self):
        self.take_effect = not self.take_effect

    def reponse_click(self):
        self.toggle_switch() 

game_start = Switch()
start_button = screen_setting.Button((400,50),"开始游戏",game_start)

def blit_start_screen():
    start_button.blit()

@screen_setting.event_check
def start_check_click(pos):
        print(start_button.check_click(pos))
        print("open:{}".format(start_button.open))

game_pause = Switch()
pause_button = screen_setting.Button((400,150),"暂停游戏",game_pause)