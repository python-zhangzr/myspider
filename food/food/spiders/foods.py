# -*- coding: utf-8 -*-
import scrapy
import os
import re
import requests
from scrapy.selector import Selector
from food.items import FoodItem
from scrapy_redis.spiders import RedisSpider
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class FoodsSpider(RedisSpider):
    name = 'foods'
    redis_key = "foodspider:start_urls"
    # allowed_domains = ['meishij.net/china-food/caixi/']
    # start_urls = ['http://meishij.net/china-food/caixi/']
     
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(FoodsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        for link in Selector(response).xpath('//dl[@class="listnav_dl_style1 w990 clearfix"]//dd//a/@href').extract():
            for i in range(80):
                fulllink=link+'?&page=%d'%i
                response = requests.get(fulllink, stream=True)
                if not response:
                    break
                yield scrapy.Request(fulllink,callback=self.parse_item1)

    def parse_item1(self, response):
        for link in Selector(response).xpath('//div[@class="listtyle1"]'):
            item=FoodItem()
            try:
                item['foodname']=link.xpath('.//div[@class="i_w"]//div[@class="c1"]/strong/text()').extract()[0]
                item['critic']=link.xpath('.//div[@class="i_w"]//div[@class="c1"]/span/text()').extract()[0].split(" ")[1]
                item['criticnum']=link.xpath('.//div[@class="i_w"]//div[@class="c1"]/span/text()').extract()[0].split(" ")[0]
                if link.xpath('.//div[@class="i_w"]//div[@class="c1"]/span/text()').extract()[0].split(" ")[4]:
                    item['popularnum']=link.xpath('.//div[@class="i_w"]//div[@class="c1"]/span/text()').extract()[0].split(" ")[3]
                    item['popular']=link.xpath('.//div[@class="i_w"]//div[@class="c1"]/span/text()').extract()[0].split(" ")[4]
                else:
                    item['popular']=link.xpath('.//div[@class="i_w"]//div[@class="c1"]/span/text()').extract()[0].split(" ")[3]
                    item['popularnum']=link.xpath('.//div[@class="i_w"]//div[@class="c1"]/span/text()').extract()[0].split(" ")[2]
                item['imageurl']=link.xpath('.//img/@src').extract()[0]
            except:
                pass
            yield item
                    


  		
