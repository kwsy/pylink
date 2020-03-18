import requests
from lxml import etree
from common.url_utils import url_to_html
import re
from db.redis_client import rpop_queue, lpush_queue
from conf.redis_conf import QueueConfig
from db.mongo_client import *
from conf.mongo_conf import MongoCollection
import time
from crawler import run_crawler_worker

def get_zhuanlan_creator_html(html):
    """
    从专栏获取个人知乎的专栏页面
    :param html:专栏html
    :return: 个人知乎专栏url
    """
    tree = etree.HTML(html)
    owner_url = tree.xpath('//a[@class = "UserLink-link"]/@href')[0][2:]
    owner_url = 'https://' + owner_url + '/columns'
    return owner_url


def get_zhuanlan_info(html):
    """
    获取专栏的关键信息, 比如专栏的名称, 关注人数
    :param html: 个人专栏页的html
    :return:
    """
    tree = etree.HTML(html)
    zhuanlan_name = tree.xpath(
        '//div[@class = "List-item"]//div[@class = "Popover"]/div[@id]/text()')  # 专栏名称，后期判断是否与python相关
    lst_html = tree.xpath('//div[@class = "List-item"]//a[@class = "ContentItem-statusItem ColumnItem-link"]/@href')
    lst_info = tree.xpath('//div[@class = "List-item"]//div[@class = "ContentItem-status"]')
    zhuanlan_html = ['https:' + i for i in lst_html]  # 专栏html

    zhuanlan_info = [research_info(lst_info[i].xpath('string(.)')) for i in range(len(lst_info))]  # 专栏信息 文章数/关注数
    blogger_name = tree.xpath('//h1[@class = "ProfileHeader-title"]/span/text()')[0]
    lst_zhuanlan = []
    zhuanlan_dict = {}
    for i in range(len(zhuanlan_name)):
        zhuanlan_dict['zhuanlan_name'] = zhuanlan_name[i]
        zhuanlan_dict['follower'] = zhuanlan_info[i][2]
        zhuanlan_dict['article_num'] = zhuanlan_info[i][1]
        zhuanlan_dict['zhuanlan_html'] = zhuanlan_html[i]
        lst_zhuanlan.append(zhuanlan_dict.copy())
    zhuanlan_ex_dict = {'blogger_name': blogger_name, 'info': lst_zhuanlan}
    return zhuanlan_ex_dict


def research_info(sentence: str):
    """
    专门解析专栏信息：例“发表xx篇文章 共xx篇文章xx人关注”，提取xx信息形成元组
    :param sentence:
    :return: (xx,xx,xx)
    """
    res = re.search(r'发表 ([0-9]+) 篇文章共 ([0-9]+) 篇文章([0-9]+) 人关注', sentence)
    res.group()
    return res.groups()


def _run_ex(url):
    """
    执行程序：专栏url→html→获取专栏主url→获取专栏主的所有专栏信息
    :return:
    """
    html = url_to_html(url)
    owner_url = get_zhuanlan_creator_html(html)
    owner_html = url_to_html(owner_url)
    lst_zhuanlan = get_zhuanlan_info(owner_html)
    return lst_zhuanlan

def test():
    """
    测试专用
    :return:
    """
    # url = 'https://zhuanlan.zhihu.com/p/109450078
    lpush_queue(QueueConfig.zhihu_queue, 'https://zhuanlan.zhihu.com/p/109450078')
    mongo_drop_collect(MongoCollection.zhihu_mongo)  # 清空表，正式时需删掉
    run()


def run(queue_name=QueueConfig.zhihu_queue, mongo_name=MongoCollection.zhihu_mongo):
    """
    执行程序逻辑：专栏url→html→获取专栏主url→获取专栏主的所有专栏信息
    :return:
    """
    run_crawler_worker(QueueConfig.zhihu_queue,MongoCollection.zhihu_mongo, _run_ex)


if __name__ == '__main__':
    url = 'https://zhuanlan.zhihu.com/c_1099248962871169024'
    test()

    # with open('../zhihu.txt', encoding='utf-8') as f:
    #     owner_url = get_zhuanlan_creator_html(f.read())
    # print(owner_url)
    # owner_html = jump_zhuanlan_owner(owner_url)
    # print(owner_html)
    # with open('../zhihu2.txt', encoding='utf-8') as f:
    #     get_zhuanlan_info(f.read())
