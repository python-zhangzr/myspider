# -*- coding: utf-8 -*-
import scrapy
from ppt.items import PptItem
from scrapy.selector import Selector


class PptzipSpider(scrapy.Spider):
    name = 'pptzip'
    allowed_domains = ['1ppt.com']
    start_urls = ['http://1ppt.com/']
    
    def parse(self, response):
        for link in Selector(response).xpath('//div[@class="w center mt4"]//div[contains(@class, "col_nav")]//ul/li[position()>1]/a/@href').extract():
            fulllink = "http://www.1ppt.com" + link
            yield scrapy.Request(fulllink, callback=self.parse_item1)

    def parse_item1(self, response):
        linkhead=response.url
        for link in Selector(response).xpath('//ul[@class="pages"]//li[position()>3]/a/@href').extract():
            fulllink = linkhead + link
            yield scrapy.Request(fulllink, callback=self.parse_item2)

    def parse_item2(self, response):
        for link in Selector(response).xpath('//div[@class="w center mt4"]//li/h2/a/@href').extract():
            fulllink = "http://www.1ppt.com" + link
            yield scrapy.Request(fulllink, callback=self.parse_item3)

    def parse_item3(self, response):
        item=PptItem()

        imagename=response.xpath('//div[@class="pleft left"]/dl//h2[1]/text()').extract()
        if len(imagename):
            item["imagename"]=imagename[0].split(" ")[0]
        else:
            item["imagename"]="NULL"

        imagelink=response.xpath('//ul[@class="downurllist"]/li/a/@href').extract()
        if len(imagelink):
            item["imagelink"]=imagelink[0]
        else:
            item["imagelink"]="NULL"
            
        yield item

        




            

