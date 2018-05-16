# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import os


BASE_PATH = os.path.abspath('..')



class LinksPipeline(object):
    def __init__(self,settings):
        self.file = open(r'%s/%s' % (BASE_PATH,settings['SAVE_FILE']), 'wb')

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
        self.file = open(r'%s/%s' % (BASE_PATH,'job_info.json'), 'wb')
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


from twisted.enterprise import adbapi
from pymysql import cursors


class MSQLPipeline(object):

    # 这个函数会自动调用
    @classmethod
    def from_settings(cls, settings):
        db_params = dict(
            host=settings["MYSQL_HOST"],
            port=settings["MYSQL_PORT"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            db=settings["MYSQL_DBNAME"],
            use_unicode=True,
            cursorclass=cursors.DictCursor
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **db_params)

        return cls(dbpool)

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.insert_sql, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print failure

    def insert_sql(self, cursor, item):
        # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
        insert_sql = """
             insert into dm_job(job_url,job_name,company_name,job_desc,
                 job_location,job_edu,language,work_year,
                 company_desc,job_salary
                 )
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_sql, (item["job_url"], item["job_name"], item["company_name"],
                                    item["job_desc"], item["job_location"], item["job_edu"],
                                    item["language"], item["work_year"], item["company_desc"], item["job_salary"]))


class MysqlTwistedPipeline(object):
    '''
    异步机制将数据写入到mysql数据库中
    '''

    # 创建初始化函数，当通过此类创建对象时首先被调用的方法
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 创建一个静态方法,静态方法的加载内存优先级高于init方法，java的static方法类似，
    # 在创建这个类的对之前就已将加载到了内存中，所以init这个方法可以调用这个方法产生的对象
    @classmethod
    # 名称固定的
    def from_settings(cls, settings):
        # 先将setting中连接数据库所需内容取出，构造一个地点
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            port=settings["MYSQL_PORT"],
            charset="utf-8",
            # 游标设置
            cursorclass=DictCursor,
            # 设置编码是否使用Unicode
            use_unicode=True
        )
        # 通过Twisted框架提供的容器连接数据库,MySQLdb是数据库模块名
        dbpool = adbapi.ConnectionPool("MySQLdb", dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用Twisted异步的将Item数据插入数据库
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 这里不往下传入item,spider，handle_error则不需接受,item,spider)

    def do_insert(self, cursor, item):
        # 执行具体的插入语句,不需要commit操作,Twisted会自动进行
        insert_sql = """
             insert into dm_job(job_url,job_name,company_name,job_desc,
                 job_location,job_edu,language,work_year,
                 company_desc,job_salary
                 )
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_sql, (item["job_url"], item["job_name"], item["company_name"],
                                    item["job_desc"], item["job_location"], item["job_edu"],
                                    item["language"], item["work_year"], item["company_desc"], item["job_salary"]))

    def handle_error(self, failure, item, spider):
        # 出来异步插入异常
        print(failure)