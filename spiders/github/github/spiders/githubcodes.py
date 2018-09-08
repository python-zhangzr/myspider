# -*- coding: utf-8 -*-
import scrapy
from github.items import GithubItem
from scrapy.selector import Selector
from scrapy import Request, FormRequest
import requests

class GithubcodesSpider(scrapy.Spider):
    name = 'githubcodes'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/']

    def start_requests(self):
        return [Request("http://github.com/login", meta = {'cookiejar' : 1}, callback = self.post_login)] 
    
    def post_login(self, response):
        return [FormRequest.from_response(response,  
                            meta = {'cookiejar' : response.meta['cookiejar']},
                            formdata = {
                            'login': '545413390@qq.com',
                            'password': 'xx31201040'
                            },
                            callback = self.after_login,
                            dont_filter = True
                            )]
    
    def after_login(self, response) :
        for url in self.start_urls :
            yield self.make_requests_from_url(url)


    def parse(self, response):
    	linkhead="/search?q=spider"
        fulllink = "http://github.com" + linkhead
        yield scrapy.Request(fulllink, callback=self.parse_item1)

    def parse_item1(self, response):
        for link in Selector(response).xpath('//div[@class="paginate-container codesearch-pagination-container"]//a/@href').extract():
            fulllink = "http://github.com" + link
            yield scrapy.Request(fulllink, callback=self.parse_item2)

    def parse_item2(self, response):
        for link in Selector(response).xpath('//div[@class="col-12 col-md-8 pr-md-3"]/h3/a/@href').extract():
            fulllink = "http://github.com" + link
            yield scrapy.Request(fulllink, callback=self.parse_item3)


    def parse_item3(self, response):
        item=GithubItem()

        imagename=response.xpath('//div[@class="Box-body p-6"]//h1[1]//text()').extract()
        if len(imagename):
            item["imagename"]=imagename[0]
        else:
            item["imagename"]="NULL"

        imagelink=response.xpath('//div[@class="mt-2"]//a[2]/@href').extract()
        if len(imagelink):
            item["imagelink"]="https://github.com" + imagelink[0]
        else:
            pass
            #item["imagelink"]="NULL"
            
        yield item
