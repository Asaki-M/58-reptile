import time, psutil, subprocess, multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from myspider.spiders.zufang import ZufangSpider

#self.spider_pid，用于存储爬虫进程的进程ID（PID）。在这里，它被硬编码为123456，在my_tk中会被终止
class Op_scrapy():
    def __init__(self):
        self.spider_pid = 123456
        # 建立线程通信管道
        self.parent_conn, self.child_conn = multiprocessing.Pipe()


#根据传入的spider_name判断要启动哪个爬虫
    def start(self, spider_name, params):
        if spider_name == 'zufang':
            spider = ZufangSpider

        else:
            return False
        self.the_scrapy = multiprocessing.Process(target=start_crawl, args=(spider, params, self.child_conn)) # 传递输入的参数以及连接pipe
        self.the_scrapy.start() # 启动新创建的进程
        self.spider_pid = self.the_scrapy.pid # 获取并保存新进程的PID
        return True



    def stop_scrapy(self):
        # 根据判断，如果scrapy还在运行，那么结束进程，
        # 同时设定爬取详情窗口的is_scrapying为False终止tree里的循环‘’‘
        if self.spider_pid in psutil.pids():  # main.py的继承类定义了该id,运行爬虫时设定
            print('scrapy还在运行！')
            time.sleep(1)
            subprocess.Popen("taskkill /pid %s /f" % self.spider_pid, shell=True)

    def check_scrapying(self):
        if self.spider_pid in psutil.pids():
            return True
        else:
            return False


def start_crawl(spider, params, pipe):
    process = CrawlerProcess(get_project_settings())
    # 将爬虫参数，通信管道参数发给scrapy，并启动
    process.crawl(spider, params=params, pipe=pipe)
    process.start()
