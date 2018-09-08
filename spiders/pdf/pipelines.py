# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
import os
import requests
from pdf import settings

class PdfPipeline(object):
    def process_item(self, item, spider):
        if 'imagelink' in item:
            images = []
            dir_path = '%s' % (settings.IMAGES_STORE)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for imagelink in item['imagelink']:
                ppt_file_name = item['imagename'] + ".rar"
                file_path1 = '%s/%s' % (dir_path, ppt_file_name)
                images.append(file_path1)
                if os.path.exists(file_path1):
                    continue
                with open(file_path1, 'wb') as handle1:
                    response = requests.get(item['imagelink'], stream=True)
                    for block in response.iter_content(1024*100):
                        if not block:
                            break
                        handle1.write(block)

           	item['imagepath'] = images
           	
        return item
