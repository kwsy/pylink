from db.mongo_client import mongo_client_insert, mongo_client_update, mongo_find_collect
from db.redis_client import rpop_queue
from conf.mongo_conf1 import MongoCollection
import time
from datetime import datetime
import logging
from common.decorator import retry
import requests
from lxml import etree

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_crawler_worker(queue_name, mongo_name, function):
    """
    执行程序:url→提取信息→存储至monogo
    :return:
    """
    while True:
        try:
            url = rpop_queue(queue_name)  # 增加去重操作
            if not url:
                time.sleep(3)
                continue
            print(url)
            if not is_need_crawler(url, mongo_name):
                continue
            content = function(url)
            print(content)
            if not content:
                time.sleep(3)
                continue
            mongo_client_update(content["href"], mongo_name, content)  # 去重操作

        except Exception as e:
            logger.info("{}消息队列".format(queue_name), e)
            time.sleep(3)


def is_need_crawler(url, mongo_name):
    if mongo_name == MongoCollection.pywebsite_mongo:
        return True
    data = mongo_find_collect(mongo_name, url)
    if data is None:
        return True
    insert_time = data['insert']

    now = datetime.now()
    diff_value = (insert_time - now).days

    if diff_value > 7:
        return True
    return False


class HttpCodeException(Exception):
    pass


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
    print(div_lst)
    if not div_lst:
        return 2 ** 32 - 1      # ?

    div = div_lst[0]
    print(div)
    text = div.xpath('string(.)')
    print(text)
    if not text:
        return 2 ** 32 - 1

    left_index = text.find('全球综合排名第')
    right_inex = text.rfind('位')
    sort = text[left_index + 7:right_inex]
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


if __name__ == "__main__":
    print(get_alexa_sort('www.zhihu.com'), type(get_alexa_sort('www.zhihu.com')))
