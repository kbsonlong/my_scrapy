import scrapy
from bs4 import BeautifulSoup
from links.items import LinksItem

class DmozSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["liepin.com"]
    start_urls = [
        "https://www.liepin.com/zhaopin/?d_sfrom=search_fp_nvbar&init=1"
    ]

    def parse(self, response):
        filename = 'links.txt'
        soups = BeautifulSoup(response.body,'lxml')
        jobObj = soups.find('ul',{'class':'sojob-list'})
        jobs = jobObj.findAll('li')
        for job in jobs:
            job_info  = job.find('div',{'class':'job-info'})
            item = LinksItem()
            # item['title'] = job_info.h3.get_text()
            item['link'] = job_info.h3.a.get('href')
            yield item

