""" 该模块提供控制终端光标输出位置的类 
    通过ANSI控制调整终端光标位置，因行位置经常出错而未能实现，未使用"""

class Cursor(object):
    """ 用于在指定的位置输出 """
    def __init__(self):
        self._row = 0
        self._column = 0

    def print_(self,text):
        """ 代替print函数 """
        print(text)
        self._row += 1
        self._column = 0

    def print_inline(self,text):
        """ 在一行内输出，请勿使用转义字符 """
        print(text,end='')
        self._column += len(str(text))

    def _up(self,row):
        for i in range(row//9):
            print('\x1b[9A',end='')
            self._row = self._row - 9
        else:
            print('\x1b[%dA' %(row%9),end='')
            self._row = self._row-(row%9)

    def _down(self,row):
        for i in range(row//9):
            print('\x1b[9B',end='')
            self._row = self._row + 9
        else:
            print('\x1b[%dB' %(row%9),end='')
            self._row = self._row+(row%9)

    def _right(self,column):
        for i in range(column//9):
            print('\x1b[9C',end='')
            self._column = self._column + 9
        else:
            print('\x1b[%dC' %(column%9),end='')
            self._column = self._column+(column%9)

    def _left(self,column):
        for i in range(column//9):
            print('\x1b[9D',end='')
            self._column = self._column - 9
        else:
            print('\x1b[%dD' %(column%9),end='')
            self._column = self._column-(column%9)

    def move_to(self,row,column):
        if row -self._row > 0:
            self._down(row - self._row)
        elif row - self._row <0:
            self._up(self._row-row)
        if column - self._column > 0:
            self._right(column - self._column)
        elif column - self._column < 0:
            self._left(self._column-column)

    def print_on(self,text,row,column):
        """ 输出到指定位置 """
        self.move_to(row,column)
        self.print_inline(text)

    """ 尝试保存光标位置，以支持模块和原生的print函数混用。因行数总是发生错误，失效
    def set_origin(self):
        self.print_inline('\x1b[s') #保存鼠标位置
        self.row = 0
        self.column = 0
       
    def restore_position(self):
        self.print_inline('\x1b[u') #还原鼠标位置
        self.row = 0
        self.column = 0
        self.print_inline('O') """


if __name__ == '__main__':
    cursor = Cursor()
    
    for i in range(10):
        cursor.print_(i*1000000)
    cursor.print_inline('x')
    cursor.move_to(3,5)
    cursor.print_inline('x')
    cursor.move_to(10,10)
    cursor.print_inline('x')
    cursor.move_to(6,3)
    cursor.print_inline('x')
    cursor.print_on('x',6,5)
    cursor.print_on('x',8,5)





#控制终端输出的参考
#https://learnku.com/articles/26231 ANSI 终端输出瞎搞指北
#https://www.zhihu.com/question/21100416/answer/208143599 python 能否print到console固定一行？