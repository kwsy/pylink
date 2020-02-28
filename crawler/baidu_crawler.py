# -*- coding:utf-8 -*-
import requests
from urllib.parse import quote
from lxml import etree


def crawler_baidu_by_keyword(keyword):
    """
    根据关键词抓取百度搜索结果
    :param keyword:
    :return: list 返回搜索结果的连接
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'referer': quote('http://www.baidu.com/s?wd=python&pn=10'),
        'Host': 'www.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }

    url = 'https://www.baidu.com/s'

    params = {
        'wd': keyword,
        'pn': 0
    }

    session = requests.session()   # 跨请求，保持某些参数
    res = session.get(url, params=params, headers=headers, allow_redirects=False)
    res.encoding = 'utf-8'

    lst = extract_links(res.text)   # 调用解析搜索连接函数

    return lst


def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html://h3[@class='t']/a@href
    :return:dict
    """
    tree = etree.HTML(html)
    a_nodes = tree.xpath("//h3[@class='t']/a[@href]")
    a_html = tree.xpath("//h3[@class='t']/a/@href")
    a_nodes_list = [i.xpath('string(.)') for i in a_nodes]

    result = {}

    for index, value in enumerate(a_nodes_list):
        result[value] = a_html[index]

    return result
if __name__ == '__main__':
    lst = crawler_baidu_by_keyword('python 教程')
    print(lst)
    # with open("../baidu.txt",encoding='utf-8')as f:
    #     extract_links(f.read())
    #     #print(f.read())