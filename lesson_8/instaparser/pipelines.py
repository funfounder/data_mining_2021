# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from pymongo import MongoClient

class InstaparserPipeline:

    def __init__(self):
        client = MongoClient('10.3.101.21', 27017)
        self.db = client['instagram_parse']

    def process_item(self, item, spider):
        collection_name = self.db[spider.name]
        #collection_name.insert_one(item)
        collection_name.update_one({"user_id": item['user_id']}, {'$set': item}, upsert=True)
        return item