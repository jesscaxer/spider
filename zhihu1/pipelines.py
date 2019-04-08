# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class Zhihu1Pipeline(object):
    def __init__(self):
        self.f = open('zhihuSpider',"a",encoding="utf-8")
    def open_spider(self):
        pass
    def process_item(self, item, spider):
        item = dict(item)
        self.f.write(json.dumps(item))
        return item
    def close_item(self):
        self.f.close()
