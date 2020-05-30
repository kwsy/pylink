import time
from conf.mongo_conf1 import MongoCollection
from db.mongo_client import mongo_find_collect_all
from common.url_utils import get_netloc
from crawler import get_alexa_sort
from db.mysql_client import *
import re
from urllib.parse import urlparse


def move_py_web_site_to_mysql():
    datas = mongo_find_collect_all(MongoCollection.pywebsite_mongo)
    for data in datas:

        print(data)
        # try:
            # netloc = get_netloc(data['href'])
            # sort = get_alexa_sort(netloc)
        # time.sleep(3)
        # url_netloc = urlparse(data['href']).netloc  # http://www.zhihu.com → www.zhihu.com
        # rank = get_alexa_sort(url_netloc)
        if not data["web_rank"]:
            data["web_rank"] = 1000000
        info = {'href': data['href'], 'web_rank': data["web_rank"], 'score': data['score'], 'insert_time': data['insert_time']}
        try:
            update_object(PyWebsite, info, 'href')
        except Exception as e:
            print(e)


def move_csdn_to_mysql():
    datas = mongo_find_collect_all(MongoCollection.csdn_mongo)
    for data in datas:
        #try:
        print(data)
        info = data
        del info['_id']
        update_object(Csdn_hjf, info, 'href')
        #except Exception as e:  # 不能用Exception太过笼统
            #print(e)


def move_zhihu_to_mysql():
    datas = mongo_find_collect_all(MongoCollection.zhihu_mongo)
    for data in datas:
        #try:
        print(data)
        for item in data['info']:
            item['insert_time'] = data['insert_time']
            item['href'] = data['href']
            item['follower'] = int(''.join(re.findall('\d+', item['follower'])))
            item['article_num'] = int(''.join(re.findall('\d+', item['article_num'])))
            print(item)
            update_object(Zhihu_hjf, item, 'zhuanlan_html')
        # except Exception as e:
        #         #     print(e)


if __name__ == '__main__':
    #move_zhihu_to_mysql()
    move_csdn_to_mysql()
    # move_py_web_site_to_mysql()
