# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PptItem(scrapy.Item):
    imagename = scrapy.Field()
    imagelink = scrapy.Field()
    imagepath = scrapy.Field()
