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


def move_csdn_to_mysql():
    datas = get_data_by_collection_name(CSDN_COLLECTION)
    for data in datas:
        info = {
            'href': data['url'],
            'original': data['original'],
            'fans': data['fans'],
            'enjoy': data['enjoy'],
            'comment': data['comment'],
            'access': data['access'],
            'grade': data['grade'],
            'week_sort': data['week_sort'],
            'score': data['score'],
            'sort': data['sort'],
            'total_socore': data['original']*10+data['fans']*20+data['enjoy']*30+data['comment']*30+data['access']*10
        }

        add_object(CSDN_COLLECTION, info)


def move_zhihu_to_mysql():
    datas = get_data_by_collection_name(ZHIHU_COLLECTION)
    for data in datas:
        for item in data['zhuanlan']:
            info = {
                # 'href': data['url'],
                'name': item['name'],
                'publish_count': item['publish_count'],
                'follow_count': item['follow_count'],
                'total_score': (item['publish_count']*50+item['follow_count']*50)
            }
            add_object(Zhihu, info)


if __name__ == '__main__':
    move_zhihu_to_mysql()