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
        info = {'href': data['url'], 'score': sort}
        add_object(PyWebsite, info)


move_py_web_site_to_mysql()