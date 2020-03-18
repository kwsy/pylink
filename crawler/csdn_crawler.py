import requests
from lxml import etree
from common.url_utils import url_to_html
from urllib.parse import urlparse
from db.redis_client import rpop_queue, lpush_queue
from conf.redis_conf import QueueConfig
from db.mongo_client import *
from conf.mongo_conf import MongoCollection
import time
from crawler import run_crawler_worker

CONTENT_NUM_CSDN = 0  # csdn导入mongo个数初始值


def get_blogger_info(html):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    {week_rank':周排名, 'sum_rank':总排名, 'original':原创, 'fans_num':粉丝,
     'like_num':获赞, 'comment_num':评论,'visit_num':访客, 'blog_level':博客等级}
    :param html: csdn.net为主信息
    :return:
    """
    tree = etree.HTML(html)
    rank = tree.xpath('//div[@class="grade-box clearfix"]/dl[@title]/@title')
    information_num = tree.xpath('//div[@class = "data-info d-flex item-tiling"]/dl[@class = "text-center"]/@title')
    blog_level = \
    tree.xpath('//div[@class="grade-box clearfix"]/dl[@class = "aside-box-footerClassify"]/dd/a/@title')[0][0]  # 博客等级
    blogger_url = tree.xpath(
        '//div[@id = "asideProfile"]//div[@class = "profile-intro-name-boxFooter"]/span/a/@href')  # 博主个人网页 me.csdn.net/XXX
    lst_info = rank + information_num + [blog_level] + blogger_url  # info形成列表
    lst_name = ['week_rank', 'sum_rank', 'original', 'fans_num', 'like_num', 'comment_num',
                'visit_num', 'blog_level', 'href']  # 定义info的名字

    csdn_dict = {}
    for index, item in enumerate(lst_name):
        csdn_dict[item] = lst_info[index]
    return csdn_dict


def get_blogger_url(url):
    """
    通常爬取到网站的csdn文章，需要实现跳转到对应博主主页
    例：‘https://blog.csdn.net/KWSY2008/article/details/103812367’
    变为‘https://blog.csdn.net/KWSY2008’
    :param url:
    :return:
    """
    url_part = urlparse(url)
    path_lst = url_part.path.split('/')
    if len(path_lst) > 1:
        path_info = path_lst[1]
        owner_url = url_part.scheme + '://' + url_part.netloc + '/' + path_info
    else:
        owner_url = url
    return owner_url


def _run_ex(url):
    """
    执行封包：获取博主url→转化为html→解析html返回字典信息
    :param url:
    :return:
    """
    owner_url = get_blogger_url(url)
    html = url_to_html(owner_url)
    csdn_dict = get_blogger_info(html)
    return csdn_dict


def test():
    """
    测试语句
    :return:
    """
    # url = 'https://blog.csdn.net/KWSY2008/article/details/103812367'    # url得用lpush_queue
    lpush_queue(QueueConfig.csdn_queue, 'https://blog.csdn.net/KWSY2008/article/details/103812367')
    mongo_drop_collect(MongoCollection.csdn_mongo)  # 清空表，正式时需删掉
    run()


def run():
    """
    执行程序:csdn url→获取作者的url→html→提取信息→该作者信息字典返回→存储至monogo
    :return:
    """
    run_crawler_worker(QueueConfig.csdn_queue, MongoCollection.csdn_mongo, _run_ex)


if __name__ == '__main__':
    # url = 'https://blog.csdn.net/KWSY2008'
    # html = url_to_html(url)
    # print(get_blogger_info)
    # with open('../csdn.txt', encoding='utf-8') as f:
    #     print(get_blogger_info(f.read()))
    # get_blogger_url("https://blog.csdn.net/KWSY2008/article/details/103812367")
    test()
    print(_run_ex('https://blog.csdn.net/KWSY2008/article/details/103812367'))