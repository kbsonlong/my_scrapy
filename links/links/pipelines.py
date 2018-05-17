# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os
from twisted.enterprise import adbapi  # 导入twisted的包
import MySQLdb
import MySQLdb.cursors
import traceback

BASE_PATH = os.path.abspath('..')


class LinksPipeline(object):
    def __init__(self,settings):
        self.file = open(r'%s/%s' % (BASE_PATH,settings['SAVE_FILE']), 'wb')

    def process_item(self, item, spider):
        line = item['link'] + "\n"
        self.file.write(line)
        return item


class PagesPipeline(object):
    def __init__(self):
        self.file = open(r'%s/%s' % (BASE_PATH,'job_info.json'), 'wb')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class MSQLPipeline(object):
    def __init__(self):  # 初始化连接mysql的数据库资源池相关信息
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                            host='www.along.party',
                                            db='cmdb',
                                            user='root',
                                            passwd='kbsonlong',
                                            port=8080,
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8',
                                            use_unicode=True
                                            )
        # pipeline dafault function                    #这个函数是pipeline默认调用的函数


    def process_item(self, item, spider):
        if spider.name == 'liepin':
            query = self.dbpool.runInteraction(self.insert_sql, item)
        elif spider.name == 'mfw':
            query = self.dbpool.runInteraction(self.do_sql, item)
        return item

    def insert_sql(self, cursor, item):
        try:
            # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
            insert_sql = """
                 insert into dm_job(job_url,job_name,company_name,job_desc,
                     job_location,edu,language,work_year,
                     company_desc,salary
                     )
                 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            cursor.execute(insert_sql, (item["job_url"], item["job_name"], item["company_name"],
                                        item["job_desc"], item["job_location"], item["job_edu"],
                                        item["language"], item["work_year"], item["company_desc"], item["job_salary"]))
        except:
            print traceback.format_exc()

    def do_sql(self, cursor, item):
        try:
            # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
            insert_sql = """
                 insert into city(cityid,city_url,city_name,nums,
                     detail,image,top1,top1_url,
                     top2,top2_url,top3,top3_url
                     )
                 VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

            cursor.execute(insert_sql,(item['cityid'],item['city_url'],item['city_name'],item['nums'],
                                       item['detail'],item['image'],item['top1'],item['top1_url'],
                                       item['top2'],item['top2_url'],item['top3'],item['top3_url']))
        except:
            print traceback.format_exc()











