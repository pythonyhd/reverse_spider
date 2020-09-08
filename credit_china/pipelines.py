# -*- coding: utf-8 -*-
import logging
import time

import pymongo

logger = logging.getLogger(__name__)


class CreditChinaPipeline(object):
    """添加必要字段"""
    def process_item(self, item, spider):
        item['spider_time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 抓取时间
        item['spider_name'] = spider.name
        item['process_status'] = 0
        item['upload_status'] = 0
        item['alter_status'] = 0
        return item


class MongodbIndexPipeline(object):
    """存储到mongodb数据库并且创建索引"""
    def __init__(self, mongo_uri, mongo_db):
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_HOST'),
            mongo_db=crawler.settings.get('MONGODB_NAME')
        )

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        # collection.create_index([('oname', 1), ('uccode', -1)])  # 1表示升序，-1降序
        collection.create_index([('stories_name', 1), ('of_company', -1)])  # 1表示升序，-1降序
        try:
            # collection.update_one({'uuid': item.get('uuid')}, {'$set': item}, upsert=True)
            collection.update_one({'stories_link': item.get('stories_link')}, {'$set': item}, upsert=True)
        except:
            logger.info('数据重复')
        return item
