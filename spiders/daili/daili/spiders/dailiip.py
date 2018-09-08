# -*- coding: utf-8 -*-
import scrapy
from daili.items import DailiItem

class DailiipSpider(scrapy.Spider):
    name = 'dailiip'
    allowed_domains = ['kuaidaili.com']
    url='https://www.kuaidaili.com/free/inha/'
    offset=1
    start_urls = [url+str(offset)+"/"]

    def parse(self, response):
        for each in response.xpath("//div[@id='list']//tbody/tr"):
            item=DailiItem()
            item['ip_port']=each.xpath("./td[1]/text()").extract()[0]+":"+each.xpath("./td[2]/text()").extract()[0]
            item['user_passwd']=""
            yield item
        if self.offset < 2043:
            self.offset+=1
        yield scrapy.Request(self.url+str(self.offset)+"/",callback=self.parse)

