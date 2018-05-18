#coding: utf8

import scrapy
import logging,traceback
from bs4 import BeautifulSoup
from links.items import LinksItem
from links.items import PagesItem


class LpSpider(scrapy.Spider):
    name = "liepin"
    allowed_domains = ["liepin.com"]
    start_urls = [
        "https://www.liepin.com/zhaopin/?d_sfrom=search_fp_nvbar&init=1"
    ]
    def parse(self, response):
        try:
            soups = BeautifulSoup(response.body,'lxml')
            jobObj = soups.find('ul',{'class':'sojob-list'})
            jobs = jobObj.findAll('li')
            for job in jobs:
                job_info  = job.find('div',{'class':'job-info'})
                ###获取到link,回调函数parse_question进行处理
                link = job_info.h3.a.get('href')
                yield scrapy.Request(link,callback=self.parse_question)
        except Exception as e:
            logging.error(traceback.format_exc())
            print e

    def parse_question(self,response):
        try:
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
            try:
                company_desc = job_info.find('div', {'class': 'info-word'}).get_text()
            except:
                company_desc = None

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
        except Exception as e:
            logging.error(traceback.format_exc())
            print e

