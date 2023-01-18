""" 控制游戏进程 """
from abc import ABCMeta, abstractmethod

class Controller(metaclass = ABCMeta):
    """ 负责游戏某一进程的控制器 """
    def __init__(self):
        pass

    @abstractmethod
    def reponse_click(self):
        """ 响应点击 """
        pass

    @abstractmethod
    def reponse_button(self):
        """ 响应按钮 """
        pass

    @abstractmethod
    def run(self):
        pass