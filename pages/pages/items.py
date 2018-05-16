# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_url = scrapy.Field()
    job_name = scrapy.Field()
    job_location = scrapy.Field()
    job_desc = scrapy.Field()
    job_edu = scrapy.Field()
    job_salary = scrapy.Field()
    language = scrapy.Field()
    work_year = scrapy.Field()
    company_name = scrapy.Field()
    company_desc = scrapy.Field()
    company_address = scrapy.Field()
    company_worktype = scrapy.Field()
    company_website = scrapy.Field()
