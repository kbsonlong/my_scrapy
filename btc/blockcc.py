#!/usr/bin/env python
# coding: utf-8
#blockcc.py
##数据爬取

import ssl,urllib2
import json
import MySQLdb,time
import ConfigParser,os
#发送带附件邮件
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import traceback

headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }



def get_api(url):
    ##避免python2.7 ssl不信任https证书验证
    context = ssl._create_unverified_context()
    req = urllib2.Request(url, headers=headers)
    response = None

    try:
        response = urllib2.urlopen(req, timeout=5, context=context)
        contexts = response.read()
        return contexts

    except urllib2.URLError as e:
        print traceback.format_exc()
        if hasattr(e, 'code'):
            print 'Error code:', e.code
            return {'code': e.code}
        elif hasattr(e, 'reason'):
            print 'Reason:', e.reason

    finally:
        if response:
            response.close()


def get_results(url,encoding='utf-8'):
    results = json.loads(get_api(url))['data']['list']
    # print result
    LT=[]
    i=0
    for result in results:
        i += 1
        T=[]
        rankd = i
        name = result['name']
        price = result['price']
        if result.has_key('zhName'):
            zh_name = result['zhName']
        else:
            zh_name = name
        volume = result['volume_ex']
        T = [x for x in [rankd,name,price,zh_name,volume]]
        LT.append(T)
    return LT


def insert_db(index=500):
    # url = "https://block.cc/api/v1/coin/list?size=%s&select=volume_ex" % index
    url = "https://block.cc/api/v1/coin/list?size=%s&type=1h&select=volume_ex&orderby=-1" % index
    # 打开数据库连接

    db = MySQLdb.connect("along_db", "root", "kbsonlong", "btchq", port=3306, charset='utf8')
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    ##获取行情数据列表
    LT = get_results(url)
    try:
        sql = "INSERT INTO currency(rankd,name,price,zh_name,volume) VALUES (%s,%s,%s,%s,%s)"
        # 执行sql语句
        cursor.executemany(sql, LT)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # Rollback in case there is any error
        print e
        db.rollback()
    # 关闭数据库连接
    db.close()
    cursor.close()


def get_context(index=50):
    url = "https://block.cc/api/v1/coin/list?size=%s&select=volume_ex" % index
    LT =  json.loads(get_api(url))['data']['list']
    contexts=[]
    i=0
    for boxContain in LT:
        i += 1
        tit = i
        name = boxContain['name']
        volume =  float(boxContain['volume_ex'])/10000
        price =  boxContain['price']
        contexts.append(u'<tr> <td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'  % (tit,name,volume,price))
    context = u'<table border="1"><tr><th>排名</th><th>名称</th><th>平均成交量(万$)</th><th>平均价格($)</th></tr> %s</table> <p>数据来源于<a href="https://block.cc">Blockcc</a><br>点击进入<a href="http://www.along.party">蜷缩的蜗牛</a><br></p> <img style="width:223px;height:223px" src="https://www.along.party/img/blog_code.png" alt="蜷缩的蜗牛博客">' % ''.join(s for s in contexts[0:index])
    return context

def sendmail(Smtp_Server,Smtp_user,Smtp_password,Subject,TO=[],files=[],context=''):
    # 实例
    msg = MIMEMultipart('alternative')
    msg['To'] = ';'.join(TO)
    msg['From'] = Smtp_user
    msg['Subject'] = Subject

    html = """\
    <html>
    <head><title>数字货币市值前一百名行情预览</title></head>
    <body>
    <p>数据来源于<a href="https://www.feixiaohao.com">非小号</a><br>
    点击进入<a href="http://www.along.party">蜷缩的蜗牛</a><br>
    </p>
    </body>
    </html>"""
    if context:
        html=context
    content = MIMEText(html, 'html', 'utf-8')
    msg.attach(content)

    # 构造附件，当多个为附件是用for读取构造
    for file in files:
        part = MIMEBase('application', 'octet-stream')  # 'octet-stream': binary data
        part.set_payload(open(file, 'rb').read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % file)
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL(Smtp_Server, 465)
        server.login(Smtp_user, Smtp_password)
        server.sendmail(Smtp_user, TO, msg.as_string())
        server.quit()
        message = 'Sendmail Success'
    except Exception, e:
        print str(e)
        message = traceback.format_exc()
    return message


def load_config(option, key):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    config = ConfigParser.ConfigParser()
    path = os.path.join(BASE_DIR, '.config.ini')
    try:
        config.read(path)
    except:
        config.read(path)
    value = config.get(option, key)
    return value

def cron_sendmail(H="09"):
    ##发送邮件
    if time.strftime("%H") == H:
        smtp_server = load_config('smtp', 'smtp_server')
        smtp_user = load_config('smtp', 'smtp_user')
        smtp_pass = load_config('smtp', 'smtp_pass')
        index = 100
        subject = u'数字货币24小时交易量前%s预览' % index
        sendto = load_config('smtp', 'sendtos').split(',')
        context = get_context(index)
        sendmail(smtp_server, smtp_user, smtp_pass, subject, sendto, context=context)

if __name__ == '__main__':
    insert_db()
    cron_sendmail()

