# -*- coding: utf-8 -*-
import scrapy


class TextgrabSpider(scrapy.Spider):
    name = 'textGrab'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://sina.com.cn/']

    def parse(self, response):
        pass
