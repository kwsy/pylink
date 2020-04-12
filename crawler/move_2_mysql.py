import time
from conf.mongo_conf1 import MongoCollection
from db.mongo_client import mongo_find_collect_all
from common.url_utils import get_netloc
from crawler import get_alexa_sort
from db.mysql_client import *
import re


def move_py_web_site_to_mysql():
    datas = mongo_find_collect_all(MongoCollection.pywebsite_mongo)
    for data in datas:
        print(data)
        try:
            netloc = get_netloc(data['href'])
            sort = get_alexa_sort(netloc)
            time.sleep(3)
            data['insert_time'] = data['insert_time'].strftime("%Y-%m-%d")
            info = {'href': data['href'], 'web_rank': sort, 'score': data['score'], 'insert_time': data['insert_time']}
            update_object(PyWebsite, info)
        except Exception as e:
            print(e)


def move_csdn_to_mysql():
    datas = mongo_find_collect_all(MongoCollection.csdn_mongo)
    for data in datas:
        try:
            data['insert_time'] = data['insert_time'].strftime("%Y-%m-%d")
            print(data)
            info = data
            del info['_id']
            update_object(Csdn_hjf, info)
        except Exception as e:
            print(e)


def move_zhihu_to_mysql():
    datas = mongo_find_collect_all(MongoCollection.zhihu_mongo)
    for data in datas:
        try:
            data['insert_time'] = data['insert_time'].strftime("%Y-%m-%d")
            print(data)
            for item in data['info']:
                item['insert_time'] = data['insert_time']
                item['href'] = data['href']
                item['follower'] = int(''.join(re.findall('\d+', item['follower'])))
                item['article_num'] = int(''.join(re.findall('\d+', item['article_num'])))
                print(item)
                update_object_zhihu(Zhihu_hjf, item)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    move_csdn_to_mysql()
    move_zhihu_to_mysql()
    move_py_web_site_to_mysql()
