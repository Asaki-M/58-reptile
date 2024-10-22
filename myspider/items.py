# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZufangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    resource = scrapy.Field()
    distance = scrapy.Field()
    price = scrapy.Field()
    community = scrapy.Field()
    area = scrapy.Field()
    room = scrapy.Field()
