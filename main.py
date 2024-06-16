from tkinter import *



from my_tk import My_tk

class MyScrapyWindow(My_tk):
    def __init__(self, tk):
        super().__init__(tk)


#定义了一个名为begin的函数，该函数的主要目的是创建一个图形用户界面窗口
def begin():
    root = Tk()
    MyScrapyWindow(root)
    root.mainloop()


if __name__ == '__main__':
    begin()
