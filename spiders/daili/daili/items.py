# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DailiItem(scrapy.Item):
    ip_port=scrapy.Field()
    user_passwd=scrapy. Field()

