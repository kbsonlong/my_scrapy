import scrapy
from bs4 import BeautifulSoup

from pages.items import PagesItem
import os,json
SAVE_FILE='links.txt'
BASE_PATH = os.path.abspath(os.path.abspath('..'))


class DmozSpider(scrapy.Spider):
    name = "pages"
    allowed_domains = ["liepin.com"]
    start_urls = []
    link_file = open(r'%s/%s' %(BASE_PATH,SAVE_FILE), 'r')
    for each_link in link_file:
        print each_link
        each_link = each_link.replace('\r', '')
        start_urls.append(each_link)
    link_file.close()

    def parse(self, response):
        soups = BeautifulSoup(response.body,'lxml')
        job_info = soups.find('div',{'class':'about-position'})
        job_name =  job_info.div.h1.get_text()
        company_name = job_info.div.h3.get_text()
        job_desc = job_info.find('div',{'class':'content content-word'}).get_text()

        item = PagesItem()
        item['job_name'] = job_name
        item['company_name'] = company_name
        item['job_desc'] = job_desc
        yield item

