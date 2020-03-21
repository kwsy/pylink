import requests
from lxml import etree
from db import redis_client
from conf.redis_conf import QueueConfig
from crawler import run_crawler_worker
from conf.mongo_conf import PY_WEB_SITE


def judge_py_website(url):
    """
    判断url是一个与python非常相关的网站
    :param url:
    :return:
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    res = requests.get(url, headers=headers)
    res.encoding = 'utf-8'

    if judge_py_site_by_keywords_description(res.text):
        return True

    if judge_py_site_by_menu(res.text):
        return True

    return False


def py_website_info(url):
    if judge_py_website(url):
        return {'url': url, 'state': True}
    else:
        return {'url': url, 'state': False}


def judge_py_site_by_keywords_description(html):
    """
    用keywords description, 判断是否是python主题网站
    :param html:
    :return:
    """
    tree = etree.HTML(html)
    if _judge_py_site_by_keywords_description_ex(tree, 'keywords'):
        return True

    if _judge_py_site_by_keywords_description_ex(tree, 'description'):
        return True

    return False


def _judge_py_site_by_keywords_description_ex(tree, tag_name):
    node_lst = tree.xpath("//meta[@name='{tag_name}']".format(tag_name=tag_name))
    if node_lst:
        node = node_lst[0]
        content = node.attrib['content'].lower()
        if content.find('python') != -1 and content.find('教程') != -1:
            return True


def judge_py_site_by_menu(html):
    """
    用菜单判断是否是python主题网站
    :param html:
    :return:
    """
    tree = etree.HTML(html)
    a_lst = tree.xpath('//li/a')
    for node in a_lst:
        text = node.text
        if len(text) <= 10 and text.lower().find('python') != -1:
            return True

    return False


def run():
    run_crawler_worker(QueueConfig.py_website, PY_WEB_SITE, py_website_info)


def test():
    redis_client.push_queue(QueueConfig.py_website, 'http://www.kidscode.cn/python')
    run_crawler_worker(QueueConfig.py_website, PY_WEB_SITE, py_website_info)


if __name__ == '__main__':
    test()
    # url = 'http://www.kidscode.cn/python'
    # print(judge_py_website(url))
    #
    # url = 'https://www.itcodemonkey.com/'
    # print(judge_py_website(url))