# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import redis
import os
import MySQLdb
import MySQLdb.cursors
import traceback,logging
from twisted.enterprise import adbapi  # 导入twisted的包
from scrapy.exceptions import DropItem
from settings import DATABASE,REDIS_CONFIG
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


Redis = redis.StrictRedis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'], db=REDIS_CONFIG['db'])
BASE_PATH = os.path.abspath('..')


class DuplicatesPipeline(object):
    """Item去重复"""
    def process_item(self, item, spider):
        if Redis.exists('url:%s' % item['url']):
            raise DropItem("Duplicate item found: %s" % item['url'])
        else:
            Redis.set('url:%s' % item['url'], REDIS_CONFIG['db'])
            return item



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
                                                host=DATABASE['host'],
                                                db=DATABASE['database'],
                                                user=DATABASE['username'],
                                                passwd=DATABASE['password'],
                                                port=DATABASE['port'],
                                                cursorclass=MySQLdb.cursors.DictCursor,
                                                charset='utf8',
                                                use_unicode=True
                                                )
            # pipeline dafault function                    #这个函数是pipeline默认调用的函数


        def process_item(self, item, spider):
            ##配置多个爬虫spider时，通过判断爬虫名称进行下一步操作
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
            except Exception as e:
                logging.error(traceback.format_exc())
                print e

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
            except Exception as e:
                logging.error(traceback.format_exc())
                print e


class ArticleDataBasePipeline(object):
    """保存文章到数据库"""

    def __init__(self):  # 初始化连接mysql的数据库资源池相关信息
        try:
            self.dbpool = adbapi.ConnectionPool('MySQLdb',
                                                host=DATABASE['host'],
                                                db=DATABASE['database'],
                                                user=DATABASE['username'],
                                                passwd=DATABASE['password'],
                                                port=DATABASE['port'],
                                                cursorclass=MySQLdb.cursors.DictCursor,
                                                charset='utf8',
                                                use_unicode=True
                                                )
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
            table_name = 'articles'
            col_str = ''
            row_str = ''
            for key in item.keys():
                col_str = col_str + " " + key + ","
                row_str = "{}'{}',".format(row_str,
                                           item[key] if "'" not in item[key] else item[key].replace("'", "\\'"))
                sql = "insert INTO {} ({}) VALUES ({}) ".format(table_name, col_str[1:-1], row_str[:-1])
            cursor.execute(sql)
            logging.info(sql)
        except:
            logging.error(traceback.format_exc())



from wordpress_xmlrpc import Client,WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost


class WordPressPipeline(object):
    def process_item(self,item,spider):
        wp = Client('https://www.along.party/xmlrpc.php', '', '')
        post = WordPressPost()
        post.title = item['title']
        # post.user = item['author']
        # post.link = item['url']
        # post.date = item['publish_time']
        # post.content = item['body']
        post.content = u"%s \n 本文转载自 <a href='%s'> %s</a> " % (item['body'], item['url'], item['title'])
        post.post_status = 'publish'
        wp.call(NewPost(post))

