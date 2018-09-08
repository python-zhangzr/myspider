# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from github.items import GithubItem
from scrapy.selector import Selector
from scrapy import Request, FormRequest
import requests

class GithubcodeSpider(CrawlSpider):
    name = 'githubcode'
    offset=1
    #url="https://github.com/search?p=%d&q=spider&type=Repositories"%offset
    #start_urls = [url]
    ssion = requests.session()
    
    def start_requests(self):
        url = 'http://github.com/login'
        '''return [scrapy.FormRequest(
            url = url,
            formdata = {'login': '545413390@qq.com','password': 'xx31201040'},
            callback = self.parse
        )]'''
        self.ssion.post(url,data = {'login': '545413390@qq.com','password': 'xx31201040'})
        response = self.ssion.get("https://github.com")
        return response


    def parse(self, response):
        url=response.url+'/search?p=%d&q=spider&type=Repositories"%offset'
        while self.offset < 100:
            #yield scrapy.Request(url, callback=self.parse_item)
            #self.make_requests_from_url(self.start_urls[0])
            self.offset=+1
            print url

    def parse_item(self, response):
        item=GithubItem()

        imagename=response.xpath('//div[@class="Box-body p-6"]//h1[1]//text()').extract()
        if len(imagename):
            item["imagename"]=imagename[0]
        else:
            item["imagename"]="NULL"

        imagelink=Selector(response).xpath('//div[@class="mt-2"]//a[2]/@href').extract()
        if len(imagelink):
            item["imagelink"]="https://github.com/" + imagelink[0]
        else:
            item["imagelink"]="NULL"
            
        yield item
