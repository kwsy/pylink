from crawler.pywebsite_crawler import get_html_from_url
from lxml import etree
import requests
import time

from conf import redis_conf
from conf import mongo_conf
from db import redis_client
from db import mongo_client

def get_url_destination(session, url):
    html = get_html_from_url(session, url)
    tree = etree.HTML(html)
    url_destination = tree.xpath("//a[@class='UserLink-link']/@href")[0]

    url_destination = "https:" + url_destination + "/columns"
    return url_destination
def get_zhuanlan_info(url):
    """
    获取一个专栏的关键信息, 比如专栏的名称, 关注人数
    :param url:
    :return:
    """
    list_allzhuanlan_info = []

    session = requests.session()
    url_destination = get_url_destination(session, url)

    html = get_html_from_url(session, url_destination)
    tree = etree.HTML(html)

    list_div_node = tree.xpath("//div[@class='List-item']")
    for div in list_div_node:
        dict_zhuanlan = {}
        zhuanlan_name = div.xpath(".//h2[@class='ContentItem-title']/a[@class='ColumnLink']/div/div/text()")[0]
        # zhuanlan_describe = div.xpath(".//div[@class='ColumnItem-meta']/text()")[0]
        zhuanlan_articlenum = div.xpath(".//div[@class='ContentItem-status']/a")[0]
        zhuanlan_articlenum = zhuanlan_articlenum.xpath('string(.)').split()[1]
        zhuanlan_url = "https:" + div.xpath(".//h2[@class='ContentItem-title']/a[@class='ColumnLink']/@href")[0]
        dict_zhuanlan['name'] = zhuanlan_name
        # dict_zhuanlan['describe'] = zhuanlan_describe
        dict_zhuanlan['articlenum'] = zhuanlan_articlenum
        dict_zhuanlan['url'] = zhuanlan_url

        list_allzhuanlan_info.append(dict_zhuanlan)
    return list_allzhuanlan_info

#　模拟测试用url
list_url_queue=["https://zhuanlan.zhihu.com/p/52580843",
                "https://zhuanlan.zhihu.com/p/36581953",
                'https://zhuanlan.zhihu.com/c_1099248962871169024',
                ]

def push_list_to_queue(queue_name, list_content):
    for content in list_content:
        redis_client.push_queue(queue_name, content)

def redis_test():
    push_list_to_queue(redis_conf.QueueConfig.zhihu_queue, list_url_queue)
    while True:
        url = redis_client.pop_queue(redis_conf.QueueConfig.zhihu_queue)
        print("url:{}".format(url))
        if  url == None:
            time.sleep(10)
            continue

        list_allzhuanlan_info = get_zhuanlan_info(url)
        print(list_allzhuanlan_info)
        mongo_client.collection_insert_many_zhihu(list_allzhuanlan_info)
        for x in mongo_client.collection_zhihu.find():
            print(x)


def zhihu_run():
    """
    从知乎redis队列中依次读取url分析获取专栏列表
    :param url:
    :return:
    """
    while True:
        url = redis_client.pop_queue(redis_conf.QueueConfig.zhihu_queue)
        print(url)
        if  url == None:
            time.sleep(10)
            continue

        list_allzhuanlan_info = get_zhuanlan_info(url)
        print(list_allzhuanlan_info)
        mongo_client.collection_insert_many_zhihu(list_allzhuanlan_info)

if __name__ == '__main__':
    redis_test()

    # zhihu_run()