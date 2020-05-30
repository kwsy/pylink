import time
from conf.mongo_conf import CSDN_COLLECTION, ZHIHU_COLLECTION, PY_WEB_SITE
from db.mongo_clinet import get_data_by_collection_name
from common.url_utils import get_url_netloc
from crawler import get_alexa_sort
from db.mysql_client import *


def move_py_web_site_to_mysql():
    datas = get_data_by_collection_name(PY_WEB_SITE)
    for data in datas:
        if not data['state']:
            continue

        netloc = get_url_netloc(data['url'])
        sort = get_alexa_sort(netloc)
        time.sleep(3)
        info = {'href': data['url'], 'total_score': sort}
        add_object(PyWebsite, info)


def move_zhihu_to_mysql():
    datas = get_data_by_collection_name(ZHIHU_COLLECTION)
    for data in datas:
        for item in data['zhuanlan']:
            publish_count = item['publish_count']
            follow_count = item['follow_count']
            score = follow_count/publish_count
            info = {
                'name': item['name'],
                'href': item['href'],
                'score': score
            }

            add_object(Zhihu, info)


def move_csdn_to_mysql():
    datas = get_data_by_collection_name(CSDN_COLLECTION)
    for data in datas:
        info = {
            'href': data['url'],
            'score': data['week_sort']
        }
        add_object(Csdn, info)

if __name__ == '__main__':
    move_csdn_to_mysql()

