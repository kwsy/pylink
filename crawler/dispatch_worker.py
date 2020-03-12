from common.url_utils import get_url_netloc
from conf.redis_conf import QueueConfig
from db import redis_client

URL_QUEUE_DICT = {
    'zhuanlan.zhihu.com': QueueConfig.zhihu_queue,
    'blog.csdn.net': QueueConfig.csdn_queue
}

def dispatch_url(url_lst):
    #  1.解析区分链接并放入队列
    for url in url_lst:
        netloc = get_url_netloc(url)
        queue_name = URL_QUEUE_DICT.get(netloc, QueueConfig.py_website)
        redis_client.sr.lpush(queue_name, url)


def get_url_lst():
    url_lst = []
    with open('../data/百度urllist.txt', encoding='utf-8') as f:
        for line in f:
            url_lst.append(line.strip())
    return url_lst


def test():
    url_lst = get_url_lst()
    dispatch_url(url_lst)
    print(redis_client.sr.rpop(QueueConfig.csdn_queue))


if __name__ == '__main__':
    test()