from lxml import etree
import requests
from db import redis_client
from conf.redis_conf import QueueConfig
from crawler import run_crawler_worker
from conf.mongo_conf import MongoConfig

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

def judge_py_website(url):
    """
    判断url是一个与python非常相关的网站
    :param url:
    :return:
    """
    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    tree = etree.HTML(res.text)

    if judge_by_keywords_description(url):
        return True

    if judge_by_menu(url):
        return True

    return False

def get_py_website_info(url):
    if judge_py_website(url):
        return {'url':url, 'state':True}
    else:
        return {'url':url, 'state':False}


def judge_by_keywords_description(url):
    if _judge_by_keywords_description(url,'keywords'):
        return True
    if _judge_by_keywords_description(url,'description'):
        return True

    return False


def _judge_by_keywords_description(url,tag):
    """
    利用Keywords，description判断网站相关性
    :param tree:
    :param tag:
    :return:
    """
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    tree = etree.HTML(res.text)
    node = tree.xpath('//meta[@name="{tag}"]'.format(tag=tag))[0]
    content = node.attrib['content'].lower()

    if content.find('python') != -1 and content.find('教程') != -1:
        return True

    return False



def judge_by_menu(url):
    """
    利用网站菜单拦判断网站相关性
    :param html:
    :return:
    """
    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'
    tree = etree.HTML(res.text)
    menu_node = tree.xpath('//ul[@id="main-menu"]/li/a')
    for menu_content in menu_node:
        content = menu_content.text.lower()
        if content.find('python') != -1 and content.find('教程') != -1:
            return True
    return False


def run():
    run_crawler_worker(QueueConfig.py_website_queue, MongoConfig.csdn_collection, get_py_website_info)


def test():
    redis_client.push_queue(QueueConfig.py_website_queue, 'http://www.kidscode.cn/python')
    run_crawler_worker(QueueConfig.py_website_queue, MongoConfig.py_website_collection, get_py_website_info)


if __name__ == '__main__':
    # url = 'http://www.kidscode.cn/python'
    # print(judge_py_website(url))
    #
    # url = 'https://www.itcodemonkey.com/'
    # print(judge_py_website(url))

    run()