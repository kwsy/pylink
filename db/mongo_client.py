from pymongo import MongoClient
from conf import mongo_conf


client = MongoClient(host=mongo_conf.mongo_setting["host"], port=mongo_conf.mongo_setting["port"])
db = client.mongo_setting["db"]

collection_zhihu = db[mongo_conf.CollectionConfig.collection_zhihu]
collection_csdn = db[mongo_conf.CollectionConfig.collection_csdn]
collection_pywebsite = db[mongo_conf.CollectionConfig.collection_pywebsite]


class MyMongoClient():
    def __init__(self):
        self.db = db
        self.collection_name = ''

    def insert_one(self, info):
        self.db[self.collection_name].insert(info)

    def insert_many(self, lst):
        self.db[self.collection_name].insert_many(lst)


class ZhihuMongo(MyMongoClient):
    def __init__(self):
        super().__init__()
        self.collection_name = mongo_conf.CollectionConfig.collection_zhihu


class CsdnMongo(MongoClient):
    def __init__(self):
        super().__init__()
        self.collection_name = mongo_conf.CollectionConfig.collection_csdn


zhihu_mongo = ZhihuMongo()
zhihu_mongo.insert_one({'name': 'python'})




def collection_insert_one(collection_name, dict_content):
    db[collection_name].insert(dict_content)

def collection_insert_many(collection_name, list_content):
    db[collection_name].insert_many(list_content)

def collection_insert_one_zhihu(dict_content):
    collection_zhihu.insert_one(dict_content)

def collection_insert_one_csdn(dict_content):
    collection_csdn.insert_one(dict_content)

def collection_insert_one_pywebsite(dict_content):
    collection_pywebsite.insert_one(dict_content)

def collection_insert_many_zhihu(list_content):
    collection_zhihu.insert_many(list_content)

def collection_insert_many_csdn(list_content):
    collection_csdn.insert_many(list_content)

def collection_insert_many_pywebsite(list_content):
    collection_pywebsite.insert_many(list_content)

def test_mongo():
    # dict_content = {'name': 'python'}
    # collection_insert_one_zhihu(dict_content)
    # collection_insert_one_csdn(dict_content)
    # collection_insert_one_pywebsite(dict_content)

    list_content = [{'name': 'python'},
                    {'name': 'zmh'}]
    collection_insert_many_zhihu(list_content)
    collection_insert_many_csdn(list_content)
    collection_insert_many_pywebsite(list_content)

    for x in collection_zhihu.find():
        print(x)
    for x in collection_csdn.find():
        print(x)
    for x in collection_pywebsite.find():
        print(x)

if __name__ == '__main__':
    test_mongo()

