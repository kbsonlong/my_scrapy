# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from settings import SAVE_FILE
# import MySQLdb

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

class PagesPipeline(object):
    def __init__(self):
        self.file = open(r'%s/job_info.txt' % (BASE_PATH), 'wb')
        # 打开数据库连接
        #self.db = MySQLdb.connect("localhost", "root", "kbsonlong", "cmdb", port=8080, charset='utf8')
        # self.db = MySQLdb.connect(host="www.along.party", port=8080, user="root", passwd="kbsonlong", db="cmdb", charset="utf8", use_unicode=True)

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)

        ###写入到数据库
        # 使用cursor()方法获取操作游标
        # cursor = self.db.cursor()
        # # SQL 插入语句
        # sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
        #        LAST_NAME, AGE, SEX, INCOME) \
        #        VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
        #       item
        # try:
        #     # 执行sql语句
        #     cursor.execute(sql)
        #     # 提交到数据库执行
        #     self.db.commit()
        # except:
        #     # Rollback in case there is any error
        #     self.db.rollback()
        #
        # # 关闭数据库连接
        # self.db.close()

        return item
