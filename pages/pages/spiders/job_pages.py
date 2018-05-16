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
        job_url = response.url
        job_info = soups.find('div',{'class':'about-position'})
        job_name =  job_info.div.h1.get_text()
        company_name = job_info.div.h3.get_text()
        job_desc = job_info.find('div',{'class':'content content-word'}).get_text()
        job_location = job_info.find('p',{'class':'basic-infor'}).span.get_text()
        job_salary = job_info.find('p',{'class':'job-item-title'}).get_text()
        job_qualifications = job_info.find('div',{'class':'job-qualifications'}).select("span")
        # print job_qualifications,type(job_qualifications)
        job_edu = job_qualifications[0].get_text()
        language = job_qualifications[2].get_text()
        work_year = job_qualifications[1].get_text()
        company_desc = job_info.find('div',{'class':'info-word'}).get_text()
        # company_address = scrapy.Field()
        # company_worktype = scrapy.Field()
        # company_website = scrapy.Field()
        item = PagesItem()
        item['job_url'] = job_url
        item['job_name'] = job_name
        item['company_name'] = company_name
        item['job_desc'] = job_desc
        item['job_location'] = job_location
        item['job_edu'] = job_edu
        item['language'] = language
        item['work_year'] = work_year
        item['company_desc'] = company_desc
        item['job_salary'] = job_salary
        yield item

