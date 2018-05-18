# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LinksItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()

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



class CityItem(scrapy.Item):
    cityid = scrapy.Field()
    city_url = scrapy.Field()
    city_name = scrapy.Field()
    nums = scrapy.Field()
    detail = scrapy.Field()
    image = scrapy.Field()
    top1 = scrapy.Field()
    top1_url = scrapy.Field()
    top2 = scrapy.Field()
    top2_url = scrapy.Field()
    top3 = scrapy.Field()
    top3_url = scrapy.Field()


class Article(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
    source_site = scrapy.Field()