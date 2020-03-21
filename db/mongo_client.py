"""
建立mongo连接
@time ： 2020年3月12日23点31分
@author : hjf
"""

import pymongo
from conf.mongo_conf import mongo_conf_hjf
import time
from datetime import datetime, timedelta

mongo_client = pymongo.MongoClient(**mongo_conf_hjf)
db = 'hjf_crawler_db'
mongo_db_hjf = mongo_client[db]


def mongo_client_insert(collection, content):
    """
    创建表collection→插入content
    :param collection: 表名
    :param content: 插入数据
    :return:
    """
    collection_hjf = mongo_db_hjf[collection]
    collection_hjf.insert(content)
    # for x in collection_hjf.find():     # 后期删掉
    #     print(x)


def mongo_client_update(href, collection, content):
    """
    对已存在的content,不重复插入，对未存在href,插入
    :param href: url地址
    :param collection:内容
    :param content:
    :return:
    """
    collection_hjf = mongo_db_hjf[collection]
    collection_hjf.update({"href": href}, {"$setOnInsert": content}, upsert=True)


def mongo_drop_collect(collection):
    """
    清空特定表
    :return:
    """
    collection_hjf = mongo_db_hjf[collection]
    collection_hjf.drop()


def judge_insert_time(href, collection, content, localtime):
    """
    判断插入时间是否大于7天,大于7天插入，不存在插入
    :return:
    """
    collection_hjf = mongo_db_hjf[collection]
    judge_info = collection_hjf.find_one({"href": href})
    if not judge_info or judge_info['insert_time']:     # 可能存在旧记录没有Insert_time，则需要更新
        mongo_client_update(href, collection, content)
    else:
        mongo_client_update(href, collection, content)
        judge_time = datetime.strptime(judge_info['insert_time'], '%Y-%m-%d')
        localtime = datetime.strptime(localtime, '%Y-%m-%d')
        if localtime - judge_time > timedelta(days=7):
            collection_hjf.remove({'href': href})
            mongo_client_update(href, collection, content)



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
    judge_insert_time(href="www.baidu.com", collection='test', content={'name': 'hjf2', 'user_info': 'python2', 'href': "www.baidu.com", 'insert_time': '2020-03-22'}, localtime='2020-04-01')
    # print('test', test)
    # print(test_collection.distinct("user_info"))

    for x in test_collection.find():
        print(x, type(x))
    test_collection.drop()

if __name__ == "__main__":
    test()