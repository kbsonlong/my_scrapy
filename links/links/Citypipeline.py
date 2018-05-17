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
import sys,six
reload(sys)
sys.setdefaultencoding("utf-8")

import logging
BASE_PATH = os.path.abspath('..')

class CityPipeline(object):
        def __init__(self):  # 初始化连接mysql的数据库资源池相关信息
            try:
                self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                                    host='www.along.party',
                                                    db='cmdb',
                                                    user='root',
                                                    passwd='kbsonlong',
                                                    port=8080,
                                                    cursorclass=MySQLdb.cursors.DictCursor,
                                                    charset='utf8',
                                                    use_unicode=True)
                logging.info('Connect DB Success !!')
            except:
                logging.error(traceback.format_exc())

        def process_item(self, item, spider):
            query = self.dbpool.runInteraction(self.do_sql, item)
            return item

            # 错误处理函数
        def handle_error(self, falure):
            print(falure)

        def do_sql(self, cursor, item):
            try:
                table_name = 'city'
                col_str = ''
                row_str = ''
                for key in item.keys():
                    col_str = col_str + " " + key + ","
                    row_str = "{}'{}',".format(row_str, item[key] if "'" not in item[key] else item[key].replace("'", "\\'"))
                    sql = "insert INTO {} ({}) VALUES ({}) ".format(table_name, col_str[1:-1],row_str[:-1])
                cursor.execute(sql)
                logging.info(sql)
            except:
                logging.error(traceback.format_exc())