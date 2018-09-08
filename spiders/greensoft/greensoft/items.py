# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class GreensoftItem(scrapy.Item):
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()
    subTitle = scrapy.Field()
    subUrls = scrapy.Field()
    littleUrls= scrapy.Field()
    softname= scrapy.Field()
    softUrl= scrapy.Field()
    subFilename=scrapy.Field()