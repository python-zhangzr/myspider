# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from pdf.items import PdfItem

class PdfsSpider(CrawlSpider):
    name = 'pdfs'
    allowed_domains = ['sj.qq.com']
    start_urls = ['http://sj.qq.com/myapp/']

    rules = (
        Rule(LinkExtractor(allow=r'.*myapp/detail\.htm.*'),callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        item=PdfItem()

        imagelink=response.xpath('//div[@class="det-ins-btn-box"]//a/@data-apkurl').extract()
        if len(imagelink)>0:
            item["imagelink"]=imagelink[0]
        else:
            pass

        imagename=response.xpath('//div[@class="det-name-int"]/text()').extract()
        if len(imagename)>0:
            item["imagename"]=imagename[0].encode("utf-8")
        else:
            pass
            
        yield item
