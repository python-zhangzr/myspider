# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class FoodItem(scrapy.Item):
    foodname = scrapy.Field()
    critic = scrapy.Field()
    criticnum = scrapy.Field()
    popular = scrapy.Field()
    popularnum= scrapy.Field()
    imageurl= scrapy.Field()
    
