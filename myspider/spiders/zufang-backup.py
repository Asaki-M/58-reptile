import scrapy
import pandas as pd
from bs4 import BeautifulSoup


class ZufangSpider(scrapy.Spider): #定义了一个名为ZufangSpider的类，它继承了Scrapy框架中的Spider类。用来爬取网站
    # Scrapy是一个用于网络爬虫的Python框架，而Spider是Scrapy中用于定义爬取行为的主要组件
    name = "zufang-backup" #设置了Spider的名字为"zufang"。这个名字在Scrapy项目中是唯一的，用于标识这个特定的爬虫。
    allowed_domains = ["gz.58.com"] #allowed_domains是一个列表，爬虫只能爬取gz.58.com这个域名下的网页。
    start_urls = ["https://gz.58.com/zufang/"] #start_urls是一个列表，包含了爬虫开始爬取的URL地址。


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml') #BeautifulSoup对象被创建，用于解析网页
        titles = soup.find_all(class_='des') #使用soup.find_all()方法，从解析后的HTML或XML中查找所有具有class属性值为'des'的元素

        data = []  # 用于存储抓取的数据的列表

        for title in titles: #遍历titles列表中的每个元素，每个元素都是一个BeautifulSoup的Tag对象，它表示一个HTML标签，该标签具有class='des'
            h2_tag = title.find('h2') #在当前title元素中查找第一个<h2>标签，并将其存储在h2_tag变量中
            jjr_tag = title.find(class_='jjr') #在当前title元素中查找第一个具有class='jjr'的标签，并将其存储在jjr_tag变量中。
            if jjr_tag: #如果找到了经纪人的tag
                jjr_par_dp_tag = jjr_tag.find(class_="jjr_par_dp") #如果找到了jjr_tag，则在该标签内部查找具有class='jjr_par_dp'和class='listjjr'的标签。
                listjjr_tag = jjr_tag.find(class_="listjjr")
                if jjr_par_dp_tag and listjjr_tag: #判断是否同时找到了jjr_par_dp_tag和listjjr_tag
                    source2 = jjr_par_dp_tag.text.strip()
                    source3 = listjjr_tag.text.strip()
                    source4 = "来自经纪人: " + source2 + ' ' + source3
                    #如果同时找到了这两个标签，则提取它们的文本内容，并去除前后的空白字符。然后，将这两个文本拼接成一个字符串，前面加上"来自经纪人:
                else:
                    source4 = "来源信息未知"
            else:
                source4 = "来源信息未知"

            if h2_tag:
                data.append({'标题': h2_tag.text.strip(), '来源': source4})
                print(f'标题{h2_tag.text.strip()},来源{source4}')

        df = pd.DataFrame(data)  # 从抓取的数据列表创建DataFrame
        df.to_excel("house.xlsx", index=False)  # 将数据保存为 Excel 文件
