from pymongo import MongoClient
from conf import mongo_conf

client = MongoClient(**mongo_conf.mongo_setting)
db = client[mongo_conf.DB_NAME]        # 数据库的名字


def insert(collection_name, info):
    db[collection_name].insert(info)