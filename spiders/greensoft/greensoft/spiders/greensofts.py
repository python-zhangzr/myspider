# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from greensoft.items import GreensoftItem
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os

class GreensoftsSpider(CrawlSpider):
    name = 'greensofts'
    allowed_domains = ['downcc.com']
    start_urls = ['http://www.downcc.com']

    rules = (
        Rule(LinkExtractor(allow=r'/sitemap.html'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'/soft/list_\d+_\d+.html')),
        Rule(LinkExtractor(allow=r'/soft/\d+.html'), callback='parse_item1'),
    )


    def parse_item(self, response):
        k=0
        parentTitle=Selector(response).xpath('//dl[@class="soft-category-bd mg-Lr10 zm"]//a[@class="name"]/text()').extract()
        for i in range(0, len(parentTitle)):
            parentFilename = "../../mygreensofts/" + parentTitle[i]
            if(not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            subTitle=Selector(response).xpath('//dl[@class="soft-category-bd mg-Lr10 zm"][%d]//dd/a/text()'%k).extract()
            for j in range(0, len(subTitle)):
                subFilename =parentFilename + '/'+ subTitle[j]
                if(not os.path.exists(subFilename)):
                        os.makedirs(subFilename)
                k+=1
    
    def parse_item1(self, response):
        item=GreensoftItem()

        imagelink=Selector(response).xpath('//div[@class="mod-list zm"]//ul[@class="ul_Address"]//li[3]/a/@href').extract()
        if len(imagelink)>0:
            item["imagelink"]=imagelink[0]
        else:
            pass

        imagename=Selector(response).xpath('//header[@class="mod-hd soft-titlebg"]//h1/text()').extract()
        if len(imagename)>0:
            item["imagename"]=imagename[0]
        else:
            pass
            
        yield item


        



