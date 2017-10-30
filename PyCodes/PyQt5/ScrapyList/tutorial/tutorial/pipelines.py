# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()

class TextPipeline(object):
    def __init__(self):
        self.limit = 50

    def process_item(self, item, spider):
        if item['text']:
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '...'
            return item
        else:
            return DropItem('Missing Text')


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class CnblogImagesPipeline(object):
    # get_project_settings().get("IMAGES_STORE")
    IMAGES_STORE = 'Images'

    def get_media_requests(self, item, info):
        image_url = item['image']
        if image_url != '':
            yield scrapy.Request(str(image_url), flags=['img'])

    def item_completed(self, result, item, info):
        image_path = [x["path"] for ok, x in result if ok]

        if image_path:
            # 重命名
            if item['name'] != None and item['name'] != '':
                ext = os.path.splitext(image_path[0])[1]
                os.rename(self.IMAGES_STORE + '/' +
                          image_path[0], self.IMAGES_STORE + '/' + item['name'] + ext)
            item["imagePath"] = image_path
        else:
            item['imagePath'] = ''
        return item
