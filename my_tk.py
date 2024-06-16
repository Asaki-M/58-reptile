import tkinter
from tkinter import *   # 从tkinter模块中导入所有可用的类和函数
import tkinter.filedialog  # 从 tkinter模块中导入filedialog 子模块
from op_scrapy import Op_scrapy  # 来源于op_scrapy文件中的Op_scrapy类
import time, threading  # 导入time模块
from tkinter import messagebox

class My_tk():  # 定义My_tk的类
    def __init__(self, tk):   # 构造函数
        self.op_scrapy = Op_scrapy()  # 创建了一个新的Op_scrapy对象，并将其保存为当前对象的op_scrapy属性
         # 界面基本设置
        self.root = tk  # 将传入的tk参数赋值给My_tk实例中的op_scrapy属性
        self.root.title("我的scrapy 爬虫")  # 窗口的标题为“我的scrapy爬虫”
        self.root.geometry("300x300")  # 创建初始爬虫功能选择按钮
        self.choice_frame = Frame(self.root)  # 创建Frame, 并将其赋值给My_tk实例中的choice_frame属性
        self.poetry_button = Button(self.choice_frame, text='爬取古诗', command=self.show_poetry)  # 创建一个Button按钮，按钮的文本设置为“爬取古诗”，按钮被点击时，会调用 My_tk 实例的 show_poetry 方法
        self.choice_frame.pack()   # 使用 pack 布局管理器将 choice_frame 框架添加到窗口中
        self.poetry_button.pack(side=LEFT)  # 使用pack布局管理器将poetry_button 按钮添加到choice_frame框架中，并设置其位置在框架的左侧
        self.zufang_button = Button(self.choice_frame, text='爬取58同城', command=self.show_zufang)
        self.zufang_button.pack(side=LEFT)
        with open('jd_status.txt', 'w') as f:
            f.write('0')


    def show_poetry(self):
        # 隐藏[选择]界面，显示为爬取【获取古诗]界面
        # self.Tid = False
        self.choice_frame.pack_forget()  # 隐藏选择界面
        self.build_poetry_frame()  # 创建【获取古诗]界面


    def build_poetry_frame(self):  # 定义名为buid_poetry_frame的方法
        # 古诗界面
        self.poetry_frame = Frame(self.root, height=50, width=100)  # 在窗口创建新的frame框架，高为50，宽为100
        self.poetry_frame.pack(anchor='center')  # 使用pack布局将self.poetry_frame宽假添加到窗口，锚点为居中
        go_back_button = Button(self.poetry_frame, text='返回', command=self.back)  # 创建返回按钮，点击时，调用self.back方法
        go_back_button.pack(anchor='w')   # 返回按钮的锚点为西，靠左对齐
        self.go_spider_button = Button(self.poetry_frame, text='爬取古诗', command=self.go_spider_poetry)  # 创建按钮，按钮文本为“爬取古诗”，点击按钮时，调用爬取古诗的方法
        self.go_spider_button.pack(anchor='center')  # 爬取古诗的按钮居中
        self.spidering_info = Listbox(self.poetry_frame, width=30)
        self.spidering_info.pack(anchor='center')  # 列表框水平居中

    def go_spider_poetry(self):
        self.spidering_info.insert('end', '开始爬虫')
        self.go_spider_button.config(state=tkinter.DISABLED)
        self.the_running_info = threading.Thread(target=self.show_running_info)
        self.the_running_info.start()
        op_result = self.op_scrapy.start('poetry')
        if op_result == False:
            self.spidering_info.insert('end', '爬虫方案有误！！！')


    def show_zufang(self):
        # 隐藏[选择]界面，显示为爬取【获取租房]界面
        # self.Tid = False
        self.choice_frame.pack_forget()  # 隐藏选择界面
        self.build_zufang_frame()


    def build_zufang_frame(self):
        # 租房页面
        self.zufang_frame = Frame(self.root, height=50, width=100)
        self.zufang_frame.pack(anchor='center')

        go_back_button = Button(self.zufang_frame, text='返回', command=self.back)
        go_back_button.pack(anchor='w')

        # 添加输入框和标签
        keyword_label = Label(self.zufang_frame, text="关键词：")
        keyword_label.pack(anchor='w')
        self.keyword_entry = Entry(self.zufang_frame, width=20)
        self.keyword_entry.pack(anchor='w')

        page_label = Label(self.zufang_frame, text="页数：")
        page_label.pack(anchor='w')
        self.page_entry = Entry(self.zufang_frame, width=10)
        self.page_entry.pack(anchor='w')

        self.go_spider_button = Button(self.zufang_frame, text='租房', command=self.go_spider_zufang)
        self.go_spider_button.pack(anchor='center')

        self.spidering_info = Listbox(self.zufang_frame, width=30)
        self.spidering_info.pack(anchor='center')


    def go_spider_zufang(self):
        try:
            page_count = int(self.page_entry.get())
            if page_count < 1:
                messagebox.showerror('错误信息', '爬取总页数不能小于1')
                return
        except:
            messagebox.showerror('错误信息', '爬取总页数必须为大于0的正整数')
            return

        self.spidering_info.insert('end', '开始爬虫')
        self.go_spider_button.config(state=tkinter.DISABLED)
        self.the_running_info = threading.Thread(target=self.show_running_info)
        self.the_running_info.start()
        # 传递页数和搜索关键词, 组成数组传递
        params = [self.keyword_entry.get(), page_count]
        op_result = self.op_scrapy.start('zufang', params)
        if op_result == False:
            self.spidering_info.insert('end,' '爬虫方案有误！！！')



    def show_running_info(self):  # 定义show_running_info的方法
        running = True  # 初始化running的值，设置值为Ture
        time1 = int(time.time())  # 获取时间，并转换为整数。存在变量time1中
        self.spidering_info.insert('end', '爬虫中线程启动')  #在 self.spidering_info的listbox的末尾插入一行文本，内容为“爬虫中... ...”
        self.spidering_info.insert('end', '爬虫中线程id:' + str(self.op_scrapy.spider_pid))
        self.spidering_info.insert('end', '爬虫线程运行中......')
        while running:
            now_time = int(time.time() - time1)
            if now_time % 2 == 0:  # now_time是偶数执行下一行代码
                if self.op_scrapy.spider_pid != 123456:
                    running = self.op_scrapy.check_scrapying()  # 调用 self.op_scrapy的check_scrapying方法，并将返回值赋给 running 变量
        
            if self.op_scrapy.parent_conn.poll():
                info_scrapy = self.op_scrapy.parent_conn.recv()
                self.spidering_info.insert('end', info_scrapy)
        self.spidering_info.insert('end', '爬虫线程关闭')
        self.go_spider_button.config(state=tkinter.NORMAL)

    def back(self):  # 定义back返回按钮的方法
        # 返回上一级选择界面，把关于诗句/简历 界面的信息、控制全部删除
        if 'poetry_frame' in dir(self):
            self.poetry_frame.destroy()  # 删除古诗界面(控件)
            delattr(self, 'poetry_frame')  # 彻底删除属性
        elif 'zufang_frame' in dir(self):
            self.zufang_frame.destroy()
            delattr(self, 'zufang_frame')
        self.choice_frame.pack()  # 显示最初的选择界面
        print(self.op_scrapy.spider_pid)
        self.op_scrapy.stop_scrapy()  # 结束exe程序
