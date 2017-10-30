# -*- coding: utf-8 -*-
import scrapy
import sys
from scrapy.spiders import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from tutorial.items import TutorialItem
import re
import tutorial.items
import json

class DoubanSpider(scrapy.spiders.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    baseUrl = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start='
    start = 0
    start_urls = [baseUrl + str(start)]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'tutorial.middlewares.ProxyMiddleWare': 1,
            #             'tutorial.middlewares.GaoxiaoSpiderMiddleware': 544
        },
        'ITEM_PIPELINES': {
            'tutorial.pipelines.CnblogImagesPipeline': 1,
        }
    }

    def parse(self, response):
        print(response.text)
        data = json.loads(response.text)['subjects']
        for i in data:
            item = tutorial.items.CnblogImageItem()
            if i['cover'] != '':
                item['image'] = i['cover']
                item['name'] = i['title']
            else:
                item['image'] = ''
            yield item
        if self.start < 400:
            self.start += 20
            yield scrapy.Request(self.baseUrl + str(self.start), callback=self.parse)
