# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from greensoft.items import GreensoftItem
import os
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class MygreensoftSpider(scrapy.Spider):
    name = 'mygreensoft'
    allowed_domains = ['downcc.com']
    start_urls = ['http://www.downcc.com/sitemap.html']

    def parse(self, response):
        for i in range(0, 27):
            item = GreensoftItem()
            parentTitle=Selector(response).xpath('//dl[@class="soft-category-bd mg-Lr10 zm"]//dt[@id="d%d"]//a[@class="name"]/text()'%i).extract()
            parentUrls=Selector(response).xpath('//dl[@class="soft-category-bd mg-Lr10 zm"]//dt[@id="d%d"]//a[@class="name"]/@href'%i).extract()
            parentFilename = "../../mygreensofts/" + parentTitle[0]
            if(not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)
            fulllink='http://www.downcc.com' + parentUrls[0]
            item['parentTitle'] = parentTitle[0]
            item['parentUrls'] = fulllink
            yield scrapy.Request(fulllink,meta={'meta_1': item},callback=self.parse_item1)

    def parse_item1(self, response):
        meta_1= response.meta['meta_1']
    	subTitle=Selector(response).xpath('//nav[@class="soft-category soft-list-category zm"]//li/a/text()').extract()
    	subUrls=Selector(response).xpath('//nav[@class="soft-category soft-list-category zm"]//li/a/@href').extract()
        for i,j in zip(range(0, len(subTitle)),range(0, len(subUrls))):
            item = GreensoftItem()
            item['parentTitle'] =meta_1['parentTitle']
            item['parentUrls'] =meta_1['parentUrls']
            subFilename ="../../mygreensofts/" + item['parentTitle'] + '/'+ subTitle[i]
            if(not os.path.exists(subFilename)):
                os.makedirs(subFilename)
            item['subTitle'] =subTitle[i]
            item['subFilename'] = subFilename
            fulllink='http://www.downcc.com' + subUrls[j]
            item['subUrls'] = subUrls[j]
            yield scrapy.Request(fulllink,meta={'meta_2':item},callback=self.parse_item2)
    
    def parse_item2(self, response):
    	meta_2= response.meta['meta_2']
    	url=response.url
    	for i in range(100):
            fulllink=re.sub(r'_\d\.html+',"_%d.html",url)%i
            response = requests.get(fulllink, stream=True)
            if not response:
                break
            yield scrapy.Request(fulllink,meta={'meta_3':meta_2},callback=self.parse_item3)

    def parse_item3(self, response):
    	meta_3= response.meta['meta_3']
    	littleUrls=Selector(response).xpath('//ul[@id="li-change-color"]/li//h3/a[1]/@href').extract()
    	for i in littleUrls:
            item = GreensoftItem()
            fulllink='http://www.downcc.com' + littleUrls[0]
            item['parentTitle'] =meta_3['parentTitle']
            item['parentUrls'] =meta_3['parentUrls']
            item['subTitle'] =meta_3['subTitle']
            item['subUrls'] = meta_3['subUrls']
            item['subFilename'] = meta_3['subFilename']
            item['littleUrls'] = fulllink
            yield scrapy.Request(fulllink,meta={'meta_4':item},callback=self.parse_item4)        	

    def parse_item4(self, response):
    	item= response.meta['meta_4']
    	softname="-".join(Selector(response).xpath('//section[@class="border mod-hd-border-cl soft-details"]//h1/text()').extract()[0].split(" "))
        if len(softname)>0:
            item["softname"]=softname
        else:
            pass
      	softUrl=Selector(response).xpath('//a[@class="soft-download soft-details-bg fl-rt download-anchor"]/@href').extract()
        if len(softUrl)>0:
            item["softUrl"]=softUrl[0]
        else:
            pass
            
        yield item
