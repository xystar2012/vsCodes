# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    movie_name = scrapy.Field()
    movie_director = scrapy.Field()
    movie_writer = scrapy.Field()
    movie_roles = scrapy.Field()
    movie_language = scrapy.Field()
    movie_date = scrapy.Field()
    movie_long = scrapy.Field()
    movie_description = scrapy.Field()
    
class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()

class CnblogImageItem(scrapy.Item):
    image = scrapy.Field()
    imagePath = scrapy.Field()
    name = scrapy.Field()

class QuoteItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
