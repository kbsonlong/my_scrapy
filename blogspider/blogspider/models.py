#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 定义数据库模型实体
Desc :
"""
import datetime

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from settings import DATABASE

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**DATABASE))


def create_news_table(engine):
    """"""
    Base.metadata.create_all(engine)


def _get_date():
    return datetime.datetime.now()


Base = declarative_base()

class ArticleRule(Base):
    """自定义文章爬取规则"""
    __tablename__ = 'article_rule'

    id = Column(Integer, primary_key=True)
    # 规则名称
    name = Column(String(30))
    # 运行的域名列表，逗号隔开
    allow_domains = Column(String(100))
    # 开始URL列表，逗号隔开
    start_urls = Column(String(100))
    # 下一页的xpath
    next_page = Column(String(100))
    # 文章链接正则表达式(子串)
    allow_url = Column(String(200))
    # 文章链接提取区域xpath
    extract_from = Column(String(200))
    # 文章标题xpath
    title_xpath = Column(String(100))
    # 文章内容xpath
    body_xpath = Column(Text)
    #文章作者xpath
    author_xpath = Column(String(150))
    # 发布时间xpath
    publish_time_xpath = Column(String(200))
    # 文章来源
    source_site = Column(String(50))
    # 规则是否生效
    enable = Column(Integer)
    """
    artile_rule3 = ArticleRule(
            name='along',
            allow_domains='along.party',
            start_urls='https://www.along.party/',
            next_page='//div[@class="pagination"]/ul/li/a',
            allow_url='/?p=\d+',
            extract_from='//div[@class="content"]',
            title_xpath='//h1[@class="article-title"]/a/text()',
            body_xpath='//article[@class="article-content"]',
            author_xpath='//span[@class="muted"][2]/a/text()'
            publish_time_xpath='//span[@class="muted"][3]',
            source_site='蜷缩的蜗牛',
            enable=0
        )
    """


class Article(Base):
    """文章类"""
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    url = Column(String(100))
    title = Column(String(100))
    body = Column(LONGTEXT)
    author = Column(String(50))
    publish_time = Column(String(200))
    source_site = Column(String(50))