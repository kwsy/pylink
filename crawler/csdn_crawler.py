import requests
from lxml import etree
from datetime import datetime
from db import redis_client
from conf.redis_conf import QueueConfig
from crawler import run_crawler_worker
from conf.mongo_conf import CSDN_COLLECTION
from db import mongo_clinet


def get_blogger_info(url):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    :param url:
    :return:
    """

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'blog.csdn.net',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    res = requests.get(url, headers=headers)
    if res is None:
        return None

    html = res.text
    info = extract_info(html)
    info['url'] = url
    info['insert_time'] = datetime.now()
    return info


def extract_info(html):
    """
    提取 个人信息
    :param html:
    :return:
    """
    # todo 处理为None的情况
    if html is None:
        pass

    tree = etree.HTML(html)
    personal_box = tree.xpath("//div[@id='asideProfile']")[0]
    basic_info = extract_basci_info(personal_box)
    grade_info = extract_grade_info(personal_box)

    info = {
        'original': csdn_int(basic_info['original']),
        'fans': csdn_int(basic_info['fans']),
        'enjoy': csdn_int(basic_info['enjoy']),
        'comment': csdn_int(basic_info['comment']),
        'access': csdn_int(basic_info['access']),
        'grade': csdn_grade(grade_info['grade']),
        'week_sort': csdn_int(grade_info['week_sort']),
        'score': csdn_int(grade_info['score']),
        'sort': csdn_int(grade_info['sort'])
    }

    return info


def csdn_grade(grade):
    index = grade.find('级')
    return int(grade[:index])


def csdn_int(value):
    index = value.find('万')
    if index != -1:
        value = int(value[:index])*10000
    else:
        value = int(value)

    return value


def extract_basci_info(personal_box):
    """
    获取博客基础信息 原创 粉丝 喜欢 评论 访问量
    :param personal_box:
    :return:
    """
    data_info = personal_box.xpath("//div[@class='data-info d-flex item-tiling']")[0]
    lst = data_info.xpath(".//dl/@title")

    data = {
        'original': lst[0],
        'fans': lst[1],
        'enjoy': lst[2],
        'comment': lst[3],
        'access': lst[4]
    }

    return data


def extract_grade_info(personal_box):
    """
    提取等级信息 等级 访问量 积分 排名
    :param personal_box:
    :return:
    """
    grade_box = personal_box.xpath("//div[@class='grade-box clearfix']")[0]
    dl_nodes = grade_box.xpath(".//dl")
    data = {
        'grade': '',
        'week_sort': '',
        'score': '',
        'sort': ''
    }

    for index, item in enumerate(dl_nodes):
        if index == 0:
            data['grade'] = item.xpath('.//a')[0].attrib['title']
        if index == 1:
            data['week_sort'] = item.attrib['title']
        if index == 2:
            data['score'] = item.xpath(".//dd")[0].attrib['title']
        if index == 3:
            data['sort'] = item.attrib['title']

    return data


def run():
    run_crawler_worker(QueueConfig.csdn_queue, CSDN_COLLECTION, get_blogger_info)


def test():
    redis_client.push_queue(QueueConfig.csdn_queue, 'https://blog.csdn.net/KWSY2008')
    run_crawler_worker(QueueConfig.csdn_queue, CSDN_COLLECTION, get_blogger_info)


if __name__ == '__main__':
    # test()
    url = 'https://blog.csdn.net/KWSY2008'
    print(get_blogger_info(url))