# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
from openpyxl import Workbook
from .items import ZufangItem


class MyspiderPipeline:
    def __init__(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='111111',
            database='nb',
            charset='utf8mb4',
        )
        self.cursor = self.conn.cursor()
        self.workbook = Workbook()
        self.worksheet = self.workbook.active
        self.worksheet.append(['title','source'])

    def process_item(self, item, spider):
        self.cursor.execute(
            """insert into myspider (title,source) values (%s,%s)""",
            (item['h2_tag'], item['source'])
        )
        self.conn.commit()
        self.worksheet.append(item['h2_tag'],item['source'])
        return item

    def close_spider(self, spider):
        self.conn.close()
