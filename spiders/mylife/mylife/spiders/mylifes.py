# -*- coding: utf-8 -*-
import scrapy
from mylife.items import MylifeItem
from scrapy.selector import Selector
import requests
from mylife import settings
import os
import re

class MylifesSpider(scrapy.Spider):
    name = 'mylifes'
    allowed_domains = ['4455pm.com']
    start_urls = ['https://www.4455pm.com/']

    def parse(self, response):
        for link in Selector(response).xpath('//div[@class="main"]//dl[@class="menu"][4]/dd/a/@href').extract():
            for i in range(1,8):
                fulllink = "https://www.4455pm.com" + link + '%d.htm'%i
                yield scrapy.Request(fulllink, callback=self.parse_item)

    def parse_item(self, response):
	for link in Selector(response).xpath('//div[@class="movie_list"]//dd/a/@href').extract():
	    fulllink = "https://www.4455pm.com" + link
	    yield scrapy.Request(fulllink, callback=self.parse_item1)

    def parse_item1(self, response):
        item=MylifeItem()
        videoname=response.xpath('//div[@class="mainArea"]/h1/text()').extract()[0]
        dir_path = '%s' % (settings.IMAGES_STORE)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        videonames= '%s/%s' % (dir_path, videoname) + ".mp4"
        if os.path.exists(videonames):
            pass 
        link = re.findall(r'var vHLSurl    = ".*\.m3u8',response.body)[0][18:-5]
        for i in range(1,2000):
            videolink=link+"%d.ts"%i
            response = requests.get(videolink, stream=True)
            if not response:
                break
            with open(videonames, 'ab+') as handle1:
                for block in response.iter_content(1024*1000):
                    if block:
                        handle1.write(block)
        print videonames + "已经下载完成"
        item["videoname"]=videonames
        yield item
       
