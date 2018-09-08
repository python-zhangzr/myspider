# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
import requests
from voa import settings

class VoaPipeline(object):  
    def process_item(self, item, spider):
        if 'imagelink' in item:
            images = []
            dir_path = '%s/%s' % (settings.IMAGES_STORE, item['mp3name'])
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for imagelink in item['imagelink']:
                image_file_name = item['mp3name'] + ".mp3"
                file_path1 = '%s/%s' % (dir_path, image_file_name)
                images.append(file_path1)
                if os.path.exists(file_path1):
                    continue
                with open(file_path1, 'wb') as handle1:
                    response = requests.get(item['imagelink'], stream=True)
                    for block in response.iter_content(1024*100):
                        if not block:
                            break
                        handle1.write(block)
            texts=[]
            text_file_name = item['mp3name'] + ".pdf"
            file_path2 = '%s/%s' % (dir_path, text_file_name)
            texts.append(file_path2)
            with open(file_path2, 'w') as handle2:
                handle2.write(item['mp3text'].encode("utf-8"))

            item['imagepath'] = images
            item['textpath'] = texts

        return item
            

 
