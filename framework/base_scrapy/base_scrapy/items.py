# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# 在这里定义你的 items，可以定义很多个 class，不同的 spiders 里面引用不同的
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BaseScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    head = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    pass