# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
import json
import requests
from food import settings
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class FoodPipeline(object):
    def process_item(self, item, spider):
    	if 'imageurl' in item:
            dir_path = '%s' % (settings.IMAGES_STORE)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for imageurl in item['imageurl']:
                file_name = item['foodname'] + ".jpg"
                file_path = '%s/%s' % (dir_path, file_name)
                if os.path.exists(file_path):
                    continue
                with open(file_path1, 'wb') as handle:
                    response = requests.get(item['imageurl'], stream=True)
                    for block in response.iter_content(1024*100):
                        if not block:
                            break
                        handle.write(block)
        return item
