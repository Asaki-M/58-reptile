import bs4
import re
import requests
import scrapy
from ..items import ZufangItem
from selenium import webdriver
import time
from loguru import logger
from selenium.webdriver.chrome.service import Service
import os

import pandas as pd

class ZufangSpider(scrapy.Spider):
    # Scrapy是一个用于网络爬虫的Python框架，而Spider是Scrapy中用于定义爬取行为的主要组件
    name = "zufang-backup" #设置了Spider的名字为"zufang"。这个名字在Scrapy项目中是唯一的，用于标识这个特定的爬虫。
    allowed_domains = ["gz.58.com"] #allowed_domains是一个列表，爬虫只能爬取gz.58.com这个域名下的网页。
    start_urls = ["https://gz.58.com/zufang/"] #start_urls是一个列表，包含了爬虫开始爬取的URL地址。


    def __init__(self, params, pipe):
        # 接收传递的参数，并赋值到 keyword，page_amount 总页数
        self.params = params
        self.keyword = params[0]
        self.page_amount = params[1]
        # 传递的不知道是啥，用来发信息到图形界面的
        self.pipe = pipe

        # 将chromedirer直接集成在项目目录下
        current_path = os.getcwd() # 获取项目根目录下的当前路径
        service = Service(executable_path=current_path+'/chromedriver/chromedriver.exe') # 拼接chromedriver的路径
        options = webdriver.ChromeOptions() # 不知道是啥，应该是默认设置 chromedriver 的参数，不用管
        self.driver = webdriver.Chrome(service=service, options=options) # 设置打开 chrome 的配置

    def parse(self, response):
        data = [] # 定义一个数据集，用来存爬取的数据
        page_num = 1 # 定义爬取的页数
        for i in range(self.page_amount):
            # 通过管道发送给tkinter爬虫进度信息
            self.pipe.send('开始爬取第 ' + str(i+1) + ' 页数据')

            # 设置 chrome driver 打开的页面地址
            self.driver.get('https://gz.58.com/zufang/pn' + str(page_num) + '?key=' + str(self.keyword))
            time.sleep(5) # 等 5 秒，方便触发反爬虫机制时候人工验证一下

            # 页数加一进入下一页
            page_num += 1
            # 获取爬到的 html 结构
            html = self.driver.page_source
            # 格式化数据
            soup = bs4.BeautifulSoup(html, 'html.parser')
            # 获取 html 中的 ul dom， 58 网页中的租房信息存在 ul 标签，类名叫 house-list
            ul_element = soup.find('ul', {'class': 'house-list'})
            # 获取 ul 标签下的所有 li 标签，也就是当前页面中每一个租房信息项
            li_elements = ul_element.find_all('li')
            # 遍历所有的 li 标签，将每一条租房信息获取
            for li_item in li_elements:
                # 跳过类名为 apartment-pkg, 这个是广告内容
                if 'apartments-pkg' in li_item.get('class', []):
                    continue
                # 58 网站中分页 dom 结构也是 li，这里跳过这个元素
                if li_item.get('id') == 'pager_wrap':
                    continue
                # 获取租房信息的标题，是一个 h2 标签
                h2_tag = li_item.find('h2')
                if h2_tag: # 存在就把标题赋值给 title
                    title = h2_tag.text.strip()
                else: # 不存在就设置一个 未知标题填充
                    title = '未知标题'

                # feat：
                # 地铁距离
                distance = '未找到距离信息'
                area = ''
                community = ''
                infor_text = ''
                infor_el = li_item.find(class_='infor')
                if infor_el:
                    infor_text = infor_el.text.strip()
                    area = infor_el.find_all('a')[0].text.strip() if infor_el.find_all('a')  else '未知区域'
                    community = infor_el.find_all('a')[1].text.strip() if len(infor_el.find_all('a')) > 1 else '未知小区'
                    
                # 使用正则表达式匹配
                match = re.search(r'距[^\s]+线-[^\s]+[\d]+m', infor_text)
                if match:
                    distance = match.group(0)
            
                # 房屋类型
                room = '未知'
                room_el = li_item.find(class_='room')
                if room_el:
                    room = room_el.text.strip()

                # 价格
                price_el = li_item.find(class_='money')
                price = '价格未知'
                if price_el:
                    price = price_el.text.strip()


                # 获取经纪人的信息 dom，是一个 div 标签，类名 jjr
                jjr_tag = li_item.find(class_='jjr')
                # 先定义一个经纪人默认的信息填充
                resource = '来源信息未知'
                if jjr_tag:
                    # jjr tag 存在
                    jjr_company_tag = jjr_tag.find(class_='jjr_par_dp') # 找到类名是 jjr_par_dp 的 dom 元素， 里面有经纪人公司信息
                    jjr_name_tag = jjr_tag.find(class_='listjjr') # 找到类名是 listjjr 的 dom 元素，里面有经纪人名字信息
                    if jjr_company_tag and jjr_name_tag: # 如果名字和公司信息存在就将上面经纪人默认的信息替换
                        jjr_company_title = jjr_company_tag.text.strip() # 通过 dom 元素的 text 来获取对应信息
                        jjr_name_title = jjr_name_tag.text.strip()
                        # 拼接信息，拼成58网页上同款展示
                        resource = '来自经纪人：' + jjr_company_title + '  ' + jjr_name_title 
                # 把找到的标题和经纪人信息存到 data 里面
                data.append({
                    '标题': title,
                    '来源': resource,
                    '地铁站距离': distance,
                    '价格': price,
                    '所在小区': community,
                    '所属区域': area,
                    '房屋类型': room,
                })

        df = pd.DataFrame(data)  # 从抓取的数据列表创建DataFrame
        df.to_excel('house.xlsx', index=False)  # 将数据保存为 Excel 文件
            
