"""
Scrapy 采集知乎的全站的粉丝信息 https://www.zhihu.com/people/ponyma/followers

    1. 数据保存在数据库

    2. 采用抓包方式

"""
# -*- coding: utf-8 -*-
import json

import requests
import scrapy
from scrapy.linkextractors import LinkExtractor


class ZhihuspiderSpider(scrapy.Spider):
    name = 'zhihuSpider'
    allowed_domains = ['www.zhihu.com']
    # for page in range(1, 3):
    #     start_urls = [f"https://www.zhihu.com/api/v4/members/ponyma/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={page}*20&limit=20 "]
    def start_requests(self):
            start_urls ="https://www.zhihu.com/api/v4/members/ponyma/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20 "
            yield scrapy.Request(start_urls, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        paging = data.get('paging')
        if paging.get('is_end') == False:
            next = paging.get('next').split(self.allowed_domains[0])
            next_url = next[0] + self.allowed_domains[0]+"/api/v4" + next[1]
            print(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            pass

        presons = data.get('data')
        for preson in presons:
            url_token = preson.get('url_token')
            name = preson.get('name')
            headline = preson.get('headline')
            item ={
                "name": name,
                "headline": headline
            }
            next = paging.get('next').split(self.allowed_domains[0])
            next_url =  f"https://www.zhihu.com/api/v4/members/{url_token}/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20 "
            yield scrapy.Request(next_url, callback=self.parse)

    #
    # def detail_parse(self, response):
    #     name = response.xpath('//h1/span[@class="ProfileHeader-name"]/text()')
    #     print(name)



