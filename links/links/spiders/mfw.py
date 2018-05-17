#coding: utf8

import scrapy,re
import logging,traceback
from bs4 import BeautifulSoup

from links.items import CityItem

class DmozSpider(scrapy.Spider):
    name = "mfw"
    allowed_domains = ["mafengwo.cn"]
    site_url = 'http://www.mafengwo.cn'
    cities_url = 'http://www.mafengwo.cn/mdd/citylist/21536.html?mddid=21536&page={page}'
    start_urls = [
        "http://www.mafengwo.cn/mdd/citylist/21536.html"
    ]
    def parse(self, response):
        try:
            soups = BeautifulSoup(response.body,'lxml')
            pattern = re.compile(r'count">共(.*?)页</span>')
            total = re.search(pattern, response.body).group(1)
            total = 2
            for i in range(1,int(total)+1):
                yield scrapy.Request(self.cities_url.format(page=i), callback=self.parse_question)
        except:
            logging.error(traceback.format_exc())
            print Exception
    def parse_question(self, response):
        try:
            soups = BeautifulSoup(response.body, 'lxml')
            for citylist in soups.findAll('li', {'class': 'item'}):
                # citylist=soups.find('li',{'class':'item'})
                item = CityItem()
                cityid = citylist.find('div', {'class': 'img'}).a.get('data-id')
                city_url = self.site_url + citylist.find('div', {'class': 'img'}).a.get('href')
                city_name = citylist.find('div', {'class': 'title'}).get_text().replace(' ', '')
                nums = citylist.find('div', {'class': 'nums'}).b.get_text()
                detail = citylist.find('div', {'class': 'detail'}).get_text().replace(' ', '')
                image = citylist.find('div', {'class': 'img'}).a.img.get('data-original')
                top1 = citylist.find('dd').select('a')[0].get_text()
                top1_url = self.site_url + citylist.find('dd').select('a')[0].get('href')
                top2 = citylist.find('dd').select('a')[1].get_text()
                top2_url = self.site_url + citylist.find('dd').select('a')[1].get('href')
                top3 = citylist.find('dd').select('a')[2].get_text()
                top3_url = self.site_url + citylist.find('dd').select('a')[2].get('href')

                item.update({'cityid': cityid, 'city_url': city_url, 'city_name': city_name, 'nums': nums,
                             'detail': detail, 'image': image, 'top1': top1, 'top1_url': top1_url,
                             'top2': top2, 'top2_url': top2_url, 'top3': top3, 'top3_url': top3_url, })

                yield item
        except:
            logging.error(traceback.format_exc())
            print Exception
