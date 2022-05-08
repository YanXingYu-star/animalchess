import screen_setting

class Switch(object):
    def __init__(self):
        self.take_effect = False

    def toggle_switch(self):
        self.take_effect = not self.take_effect
            
class Button(object):
    def __init__(self,rect,text,switch=None):
        self.rect=rect  #按键的矩形(left,top,width,height) 
        self.text = text   #
        self.status = 1     #1：按钮可以按
        self.open = 0   #1：按钮开启 0：按钮关闭
        self.switch:Switch = switch
    
    def open_me(self):
        self.open = not self.open
        if self.switch != None:
            self.switch.toggle_switch()

    def pos_in_rect(self,pos):
        if pos[0]>self.rect[0] and pos[0]<self.rect[0]+self.rect[2]:
            if pos[1]>self.rect[1] and pos[1]<self.rect[1]+self.rect[3]:
                return True
        else:
            return False

    def is_click(self,click_pos):
        if self.status == 0:
            return False
        else:
            if self.pos_in_rect(click_pos):   #判断pos是否在self.rect内
                self.open_me()
            return self.pos_in_rect(click_pos)


    def check_click(self,pos):

            return self.is_click(pos)

    @property
    def blit_parameter(self):
        """ 返回pygame.blit所需的一些参数 """
        return (self.text,self.rect)

    def blit(self):
        screen_setting.fill_background()
        screen_setting.blit_text(*self.blit_parameter)
        screen_setting.update()


