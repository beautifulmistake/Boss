# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 搜索关键字
    search_key = scrapy.Field()
    # 公司的名称
    company_name = scrapy.Field()
    # 公司信息
    info = scrapy.Field()

