# coding: utf-8
#blockcc.py
#web展示
import ssl,urllib2
import json,time,traceback,datetime
import MySQLdb
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/line-stack.html')
def index():
    return render_template('line-stack.html')
@app.route('/test')
def test():
    return render_template('line-stack-bak.html')

@app.route('/select')
def select_db():
    # 打开数据库连接
    try:
        name = request.args.get('name')
        start_time = request.args.get('starttime')
        endt_ime = request.args.get('endtime')
    except:
        name = "Bytom"
    endt_ime= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start_time= (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d %H:%M:%S")

    # db = MySQLdb.connect("along_db", "root", "kbsonlong", "btchq", port=3306, charset='utf8')
    db = MySQLdb.connect("172.96.247.193", "root", "kbsonlong", "spider_tools", port=8080, charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    ##获取行情数据列表
    try:
        sql = '''SELECT price,create_time FROM currency WHERE NAME = "%s"
        AND create_time BETWEEN "%s"  AND "%s" ORDER BY create_time ''' % (name,start_time,endt_ime)
        print sql
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        results = cursor.fetchall()
        TimeList = []
        PriceList = []
        for row in results:
            TimeList.append(row[1].strftime("%Y-%m-%d %H:%M:%S"))
            PriceList.append(row[0])
        return json.dumps({'TL':TimeList,'PL':PriceList,'name':name})
    except Exception as e:
        # Rollback in case there is any error
        print traceback.format_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()
    cursor.close()

@app.route('/select2')
def mult_select():
    try:
        limit = request.args.get('limit')
    except:
        limit = 10
    # db = MySQLdb.connect("along_db", "root", "kbsonlong", "btchq", port=3306, charset='utf8')
    db = MySQLdb.connect("172.96.247.193", "root", "kbsonlong", "spider_tools", port=8080, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    ##获取价格排名前十
    sql = "SELECT name from currency ORDER BY create_time,price desc LIMIT %s" % limit
    cursor.execute(sql)
    # 提交到数据库执行
    names = cursor.fetchall()
    L = []
    try:
        for name in names:
            sql = '''SELECT price,create_time FROM currency WHERE NAME = "%s"
            AND create_time  ORDER BY create_time ''' % (name[0])
            # print sql
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            results = cursor.fetchall()
            TimeList = []
            PriceList = []
            for row in results:
                TimeList.append(row[1].strftime("%Y-%m-%d %H:%M:%S"))
                PriceList.append(row[0])
            dd = {'prices': PriceList, 'name': name[0]}
            L.append(dd)
    except Exception as e:
        print e
        db.rollback()
    finally:
        # 关闭数据库连接
        db.close()
        cursor.close()
    return json.dumps({"PL": L, "TL": TimeList})


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')