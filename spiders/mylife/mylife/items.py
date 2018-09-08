# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MylifeItem(scrapy.Item):
    videoname = scrapy.Field()
    videolink = scrapy.Field()
