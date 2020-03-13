from pymongo import MongoClient
from conf import mongo_conf


client = MongoClient(host=mongo_conf.mongo_setting["host"], port=mongo_conf.mongo_setting["port"])
db = client.mongo_setting["db"]

collection_zhihu = db[mongo_conf.CollectionConfig.collection_zhihu]
collection_csdn = db[mongo_conf.CollectionConfig.collection_csdn]
collection_pywebsite = db[mongo_conf.CollectionConfig.collection_pywebsite]

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

