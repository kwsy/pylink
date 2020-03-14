"""
建立mongo连接
@time ： 2020年3月12日23点31分
@author : hjf
"""

import pymongo
from conf.mongo_conf import mongo_conf_hjf

mongo_client = pymongo.MongoClient(**mongo_conf_hjf)


def mongo_client_insert(collection, content):
    """
    建立mongo连接→进入数据库→创建表collection→插入content
    :param collection: 表名
    :param content: 插入数据
    :return:
    """
    mongo_db_hjf = mongo_client['hjf_crawler_db']
    collection_hjf = mongo_db_hjf[collection]
    collection_hjf.insert(content)
    for x in collection_hjf.find():     # 后期删掉
        print(x)

def mongo_drop_collect(collection):
    """
    清空特定表
    :return:
    """
    mongo_db_hjf = mongo_client['hjf_crawler_db']
    collection_hjf = mongo_db_hjf[collection]
    collection_hjf.drop()


def test():
    """
    测试专用
    :return:
    """
    mongo_client_hjf = pymongo.MongoClient(**mongo_conf_hjf)
    mongo_db_hjf = mongo_client_hjf['hjf_db']
    test_collection = mongo_db_hjf['test']
    test_collection.insert([{'name': 'hjf', 'user_info': 'python'}, {'name': 'hjf2', 'user_info': 'python2'}])
    test = test_collection.find_one()
    print(test)
    print(test_collection.distinct("user_info"))

    for x in test_collection.find():
        print(x, type(x))
    test_collection.drop()

if __name__ == "__main__":
    test()