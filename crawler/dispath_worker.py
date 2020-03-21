from urllib.parse import urlparse
from db import redis_client
from conf.redis_conf import QueueConfig
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


queue_path = {'zhuanlan.zhihu.com': QueueConfig.zhihu_queue, 'blog.csdn.net': QueueConfig.csdn_queue}   # 消息队列字典映射


def dispath_url(url_lst: list):
    """
    识别队列中不同的url,始终是单个传入
    :param url_lst:list
    :return:
    """
    for url in url_lst:
        netloc_url = urlparse(url).netloc
        queue_name = queue_path.get(netloc_url, QueueConfig.pywebsite_queue)    # 通过字典获取对应QueueName
        redis_client.lpush_queue(queue_name, url)
    return


def test_get_url():
    """
    获取测试数据集
    :return:
    """
    with open('../data/urlfile/url汇总/百度搜索分析url内容_url汇总', encoding='utf-8') as f:
        url_lst = []
        for line in f:
            url_lst.append(line.strip())
        print(url_lst)
    return url_lst


def test_dispath_url():
    """
    测试dispath_url函数
    :return:
    """
    url = ['https://zhuanlan.zhihu.com/question/267972964?sort=created']
    dispath_url(url)
    print(redis_client.connect_redis.rpop(QueueConfig.zhihu_queue))


if __name__ == "__main__":
    test_dispath_url()