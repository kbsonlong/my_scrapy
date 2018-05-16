# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os,json

BASE_PATH = os.path.abspath('..')

class PagesPipeline(object):
    def __init__(self):
        self.file = open(r'%s/job_info.txt' % (BASE_PATH), 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
