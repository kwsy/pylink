import time
from conf.mongo_conf1 import MongoCollection
from db.mongo_client import mongo_find_collect_all
from common.url_utils import get_netloc
from crawler import get_alexa_sort
from db.mysql_client import *


def move_py_web_site_to_mysql():
    datas = mongo_find_collect_all(MongoCollection.pywebsite_mongo)
    for data in datas:
        netloc = get_netloc(data['href'])
        sort = get_alexa_sort(netloc)
        time.sleep(3)
        data['insert_time'] = data['insert_time'].strftime("%Y-%m-%d")
        info = {'href': data['href'], 'web_rank': sort, 'score': data['score'], 'insert_time': data['insert_time']}
        update_object(PyWebsite, info)


move_py_web_site_to_mysql()