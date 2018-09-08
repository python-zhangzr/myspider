# -*- coding: utf-8 -*-
import scrapy
from voa.items import VoaItem
from scrapy.selector import Selector

class Voamp3Spider(scrapy.Spider):
    name = 'voamp3'
    allowed_domains = ['51voa.com']
    start_urls = ['http://51voa.com/']
    
    def parse(self, response):
        for link in Selector(response).xpath('//div[@id="left_nav"]//ul[2]/li/a/@href').extract():
            fulllink = "http://www.51voa.com" + link
            yield scrapy.Request(fulllink, callback=self.parse_item1)

    def parse_item1(self, response):
        for link in Selector(response).xpath('//div[@id="pagelist"]//a/@href').extract():
            fulllink = "http://www.51voa.com/" + link
            yield scrapy.Request(fulllink, callback=self.parse_item2)

    def parse_item2(self, response):
        for link in Selector(response).xpath('//div[@id="list"]//ul/li/a/@href').extract():
            fulllink = "http://www.51voa.com" + link
            yield scrapy.Request(fulllink, callback=self.parse_item3)

    def parse_item3(self, response):
        item=VoaItem()

        mp3name=response.xpath('//div[@id="title"]/h1/text()').extract()
        if len(mp3name):
            item["mp3name"]=mp3name[0]
        else:
            item["mp3name"]="NULL"

        mp3text=response.xpath('//div[@id="content"]/p/text()').extract()
        if len(mp3text):
            item["mp3text"]="\n".join(mp3text)
        else:
            item["mp3text"]="NULL"

        imagelink=response.xpath('//div[@id="menubar"]/a[1]/@href').extract()
        if len(imagelink):
            item["imagelink"]=imagelink[0]
        else:
            item["imagelink"]="NULL"
            
        yield item

        #yield scrapy.Request(imagelink, callback=self.parse_item4)




            

