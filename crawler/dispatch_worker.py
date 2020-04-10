from db import redis_client
from db.redis_client import QueueConfig
from common import url_utils


URL_QUEUE_DICT ={
                'zhuanlan.zhihu.com':QueueConfig.zhihu_queue,
                 'blog.csdn.net':QueueConfig.csdn_queue,
}

def dispatch_url(url_lst):
    '''
    识别url_lst里的url，push不同的消息队列
    :param url_lst:
    :return:
    '''
    for url in url_lst:
        netloc = url_utils.get_url_netloc(url)
        print(netloc)     #测试函数。解析网址是否正确
        queue_name = URL_QUEUE_DICT.get(netloc,QueueConfig.py_website)
        redis_client.push_queue(queue_name,url)

        # if netloc =='zhuanlan.zhihu.com':
        #     redis_client.push_queue(QueueConfig.zhihu_queue,url)   #push到不同的消息队列里面
        #
        # elif netloc == 'blog.csdn,net':
        #     redis_client.push_queue(QueueConfig.csdn_queue, url)
        #
        # else:
        #     redis_client.push_queue(QueueConfig.py_website,url)


def get_url_lst():#测试
    url_lst=[]
    with open('baidu_result.txt','r')  as  f:#需要百度检索的网址数据
        for line in f:
           url_lst.append(line.strip())

    return url_lst


def test():
    url_lst = get_url_lst()
    dispatch_url(url_lst)


if __name__ == '__main__':
    test()
