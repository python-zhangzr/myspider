# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VoaItem(scrapy.Item):
    mp3name = scrapy.Field()
    mp3text = scrapy.Field()
    imagelink = scrapy.Field()
    imagepath = scrapy.Field()
    textpath = scrapy.Field()
