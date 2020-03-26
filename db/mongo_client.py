"""
建立mongo连接
@time ： 2020年3月12日23点31分
@author : hjf
"""

import pymongo
from conf.mongo_conf1 import mongo_conf_hjf, db

mongo_client = pymongo.MongoClient(**mongo_conf_hjf)
mongo_db_hjf = mongo_client[db]


def mongo_client_insert(collection, content):
    """
    创建表collection→插入content
    """
    mongo_db_hjf[collection].insert(content)


def mongo_client_update(href, collection, content):
    """
    对已存在的content,不重复插入，对未存在href,插入
    """
    mongo_db_hjf[collection].update({"href": href}, {"$setOnInsert": content}, upsert=True)


def mongo_drop_collect(collection):
    """
    清空特定表
    """
    mongo_db_hjf[collection].drop()


def mongo_find_collect(collection, href):
    """
    查找href
    """
    return mongo_db_hjf[collection].find_one({"href": href})


def mongo_remove_one(collection, href):
    """
    删除href对应信息
    """
    return mongo_db_hjf[collection].remove({"href": href})


def test():
    """
    测试专用
    :return:
    """
    mongo_client_hjf = pymongo.MongoClient(**mongo_conf_hjf)
    mongo_db_hjf = mongo_client_hjf['hjf_crawler_db']
    test_collection = mongo_db_hjf['test']
    test_collection.update({"href": "www.baidu.com"}, {"$setOnInsert": {'name': 'hjf2', 'user_info': 'python2', 'href': "www.baidu.com", 'insert_time': '2020-03-21'}}, upsert=True)
    test_collection.update({"href": "www.baidu.com"}, {"$setOnInsert": {'name': 'hjf5', 'user_info': 'python1', 'href': 'www.baidu.com', 'insert_time': '2020-03-23'}}, upsert=True)
    print(test_collection.find_one({"href": "www.baidu.com"})['href'])
    #test_collection.remove({"href": "www.baidu.com"})
    # print('test', test)
    # print(test_collection.distinct("user_info"))

    for x in test_collection.find():
        print(x, type(x))
    test_collection.drop()

if __name__ == "__main__":
    test()