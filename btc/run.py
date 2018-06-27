# coding: utf-8
#blockcc.py
#web展示
import ssl,urllib2
import json
import MySQLdb
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/line-stack.html')
def index():
    return render_template('line-stack.html')

@app.route('/select')
def select_db():
    # 打开数据库连接
    try:
        name = request.args.get('name')
    except:
        name = "Bytom"

    # db = MySQLdb.connect("along_db", "root", "kbsonlong", "btchq", port=3306, charset='utf8')
    db = MySQLdb.connect("172.96.247.193", "root", "kbsonlong", "spider_tools", port=8080, charset='utf8')

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    ##获取行情数据列表
    try:
        sql = 'SELECT price,create_time FROM currency  WHERE name = "%s" ORDER  BY create_time ' % name
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
        print e
        db.rollback()
    # 关闭数据库连接
    db.close()
    cursor.close()


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')