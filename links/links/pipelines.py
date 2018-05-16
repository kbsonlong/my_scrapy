# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from settings import SAVE_FILE

BASE_PATH = os.path.abspath('..')



class LinksPipeline(object):
    def __init__(self):
        self.file = open(r'%s/%s' % (BASE_PATH,SAVE_FILE), 'wb')

    def process_item(self, item, spider):
        line = item['link'] + "\n"
        self.file.write(line)
        return item

class JsonWriterPipeline(object):

    def __init__(self):
        self.file = open(r'%s/%s' % (BASE_PATH,SAVE_FILE), 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item