import time
import requests
from lxml import etree
from datetime import datetime
from db.redis_client import pop_queue
from db.mongo_clinet import insert, get_data_by_url
from conf import mongo_conf
from functools import wraps

def run_crawler_worker(queue_name, collection_name, function):
    while True:
        url = pop_queue(queue_name)
        if not url:
            time.sleep(3)
            continue

        if not is_need_crawler(url, collection_name):
            continue

        print(url)
        info = function(url)
        if not info:
            time.sleep(3)
            continue

        insert(collection_name, info)


def retry(retry_count=5, sleep_time=1):
    def wrapper(func):
        @wraps(func)
        def inner(*args,**kwargs):
            for i in range(retry_count):
                try:
                    res = func(*args,**kwargs)
                    return res
                except:
                    time.sleep(sleep_time)
                    continue
            return None
        return inner
    return wrapper

class HttpCodeException(Exception):
    pass

def is_need_crawler(url, collection_name):
    if collection_name == mongo_conf.PY_WEB_SITE:
        return True

    data = get_data_by_url(collection_name, url)

    if data is None:
        return True

    insert_time = data['insert_time']
    now = datetime.now()

    day_diff = (now - insert_time).days
    if day_diff > 7:
        return True

    return False


@retry(sleep_time=3)
def get_alexa_sort_ex(netloc):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    url = 'https://alexa.chinaz.com/detail.asp'
    params = {'domain': netloc}
    res = requests.get(url, params=params, headers=headers)
    tree = etree.HTML(res.text)

    div_lst = tree.xpath("//div[@class='row_title clearfix']")
    if not div_lst:
        return 2**32 -1

    div = div_lst[0]
    text = div.xpath('string(.)')
    if not text:
        return 2**32 -1

    left_index = text.find('全球综合排名第')
    right_inex = text.rfind('位')
    sort = text[left_index+7:right_inex]
    return int(sort)

@retry(sleep_time=3)
def get_alexa_sort(netloc):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    url = 'http://www.alexa.cn/rank/' + netloc
    res = requests.get(url, headers=headers)
    token_index = res.text.find('token')
    domain_index = res.text.find('domain', token_index)
    token = res.text[token_index + len("token : '"): domain_index - 3]

    # domain_left = res.text.find("'", domain_index)
    # domain_right = res.text.find("'", domain_left+1)
    # domain = res.text[domain_left+1:domain_right]
    url = 'http://www.alexa.cn/api/alexa/free'

    params = {'token': token, 'url': netloc}
    res = requests.get(url, params, headers=headers)
    data = res.json()

    return data['data']['world_rank']