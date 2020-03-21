from pymongo import MongoClient
from conf import mongo_conf

client = MongoClient(**mongo_conf.mongo_setting)
db = client[mongo_conf.DB_NAME]        # 数据库的名字


def insert(collection_name, info):
    url = info['url']
    db[collection_name].update({'url': url}, info, upsert=True)


def get_data_by_url(collection, url):
    return db[collection].find_one({'url': url})

