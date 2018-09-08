# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
import json
import requests
from greensoft import settings
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class GreensoftPipeline(object):
    def __init__(self):
        self.file = open('green.json', 'wb')
    def process_item(self, item, spider):
        softname= item["softname"]
        softUrl= item["softUrl"]
        subFilename=item['subFilename']
        file_name = subFilename + '/' + softname
        if os.path.exists(file_name):
            pass
        try:
            with open(file_name, 'wb') as handle1:
                response = requests.get(softUrl, stream=True)
                #if not response:
                    #exit()
                for block in response.iter_content(1024*100):
                    if not block:
                        break
                    handle1.write(block)
        except:
            content = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(content)    
        return item
    def close_spider(self, spider):
        self.file.close()
