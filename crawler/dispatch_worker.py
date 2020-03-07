from db import redis_client
from conf.redis_conf import QueueConfig
from common import url_utils


URL_QUEUE_DICT = {
    'zhuanlan.zhihu.com': QueueConfig.zhihu_queue,
    'blog.csdn.net': QueueConfig.csdn_queue
}

def dispatch_url(url_lst):
    """
    识别url_lst里的url，push到不同的消息队列
    :param url_lst:
    :return:
    """
    for url in url_lst:
        netloc = url_utils.get_url_netloc(url)
        queue_name = URL_QUEUE_DICT.get(netloc, QueueConfig.py_website_queue)
        redis_client.push_queue(queue_name, url)

    #     if netloc == 'zhuanlan.zhihu.com':
    #         redis_client.push_queue(QueueConfig.zhihu_queue, url)
    #     elif netloc == 'blog.csdn.net':
    #         redis_client.push_queue(QueueConfig.csdn_queue, url)
    #     else:
    #         redis_client.push_queue(QueueConfig.py_website_queue, url)



def get_url_lst():
    url_lst = []
    with open('../data/urlfile/url汇总/百度搜索分析url内容_url汇总') as f:
        for line in f:
            url_lst.append(line.strip())

    return url_lst

def test():
    url_lst = get_url_lst()
    dispatch_url(url_lst)



if __name__ == '__main__':
    test()