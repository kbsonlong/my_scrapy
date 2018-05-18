#coding: utf8
##运行爬虫

import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from links.spiders.mfw import MfwSpider
from links.spiders.liepin import LpSpider

if __name__ == '__main__':
    settings = get_project_settings()

    configure_logging()
    runner = CrawlerRunner(settings)

    runner.crawl(MfwSpider)
    runner.crawl(LpSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()
