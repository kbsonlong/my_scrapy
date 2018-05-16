import scrapy
from bs4 import BeautifulSoup
from links.items import LinksItem
from links.items import PagesItem

class DmozSpider(scrapy.Spider):
    name = "links"
    allowed_domains = ["liepin.com"]
    start_urls = [
        "https://www.liepin.com/zhaopin/?d_sfrom=search_fp_nvbar&init=1"
    ]

    def parse(self, response):
        soups = BeautifulSoup(response.body,'lxml')
        jobObj = soups.find('ul',{'class':'sojob-list'})
        jobs = jobObj.findAll('li')
        for job in jobs:
            job_info  = job.find('div',{'class':'job-info'})
            item = LinksItem()
            # item['title'] = job_info.h3.get_text()
            link = job_info.h3.a.get('href')
            yield scrapy.Request(link,callback=self.parse_question)
            # yield item

    def parse_question(self,response):
        soups = BeautifulSoup(response.body, 'lxml')
        job_url = response.url
        job_info = soups.find('div', {'class': 'about-position'})
        job_name = job_info.div.h1.get_text()
        company_name = job_info.div.h3.get_text()
        job_desc = job_info.find('div', {'class': 'content content-word'}).get_text()
        job_location = job_info.find('p', {'class': 'basic-infor'}).span.get_text()
        job_salary = job_info.find('p', {'class': 'job-item-title'}).get_text()
        job_qualifications = job_info.find('div', {'class': 'job-qualifications'}).select("span")
        job_edu = job_qualifications[0].get_text()
        language = job_qualifications[2].get_text()
        work_year = job_qualifications[1].get_text()
        company_desc = job_info.find('div', {'class': 'info-word'}).get_text()
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

