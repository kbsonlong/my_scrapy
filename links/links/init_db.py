#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from models import db_connect,create_news_table
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from models import ArticleRule

@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def init_rule():
    engine = db_connect()
    create_news_table(engine)
    Session = sessionmaker(bind=engine)
    with session_scope(Session) as session:
        artile_rule1 = ArticleRule(
            name='huxiu',
            allow_domains='huxiu.com',
            start_urls='http://www.huxiu.com/',
            next_page='',
            allow_url='/article/\d+/\d+\.html',
            extract_from='//div[@class="mod-info-flow"]',
            title_xpath='//div[@class="article-wrap"]/h1/text()',
            body_xpath='//div[@id="article_content"]/p//text()',
            author_xpath='//span[@class="muted"][2]/a/text()',
            publish_time_xpath='//span[@class="article-time"]/text()',
            source_site='虎嗅网',
            enable=0
        )
        artile_rule2 = ArticleRule(
            name='osc',
            allow_domains='oschina.net',
            start_urls='http://www.oschina.net/',
            next_page='',
            allow_url='/news/\d+/',
            extract_from='//div[@id="IndustryNews"]',
            title_xpath='//h1[@class="OSCTitle"]/text()',
            author_xpath='//span[@class="muted"][2]/a/text()',
            publish_time_xpath='//div[@class="PubDate"]/text()',
            body_xpath='//div[starts-with(@class, "Body")]/p[position()>1]//text()',
            source_site='开源中国',
            enable=0
        )
        artile_rule3 = ArticleRule(
            name='along',
            allow_domains='along.party',
            start_urls='https://www.along.party/',
            next_page='',
            allow_url='/?p=\d+',
            extract_from='//div[@class="content"]',
            title_xpath='//h1[@class="article-title"]/a/text()',
            body_xpath='//div[@class="post-content"]',
            author_xpath='//span[@class="muted"][2]/a/text()',
            publish_time_xpath='//span[@class="muted"]/text()',
            source_site='蜷缩的蜗牛',
            enable=1
        )
        session.add(artile_rule1)
        session.add(artile_rule2)
        session.add(artile_rule3)

if __name__ == '__main__':
    init_rule()