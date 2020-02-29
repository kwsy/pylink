import time
from lxml import etree
import requests
from urllib.parse import quote
from conf import crawler_config
from conf.bd_keywords import keyword_lst


def run():
    """
    爬虫启动脚本
    :return:
    """
    url_lst = crawler_all_keywords(keyword_lst)
    print(url_lst)


def crawler_all_keywords(keyword_lst):
    """
    抓取所有关键词搜索出来的网页中涉及的网址
    :param keyword_lst:
    :return:
    """
    all_url_lst = []
    for keyword in keyword_lst:
        lst = crawler_baidu_by_keyword(keyword)
        all_url_lst.extend(lst)

    return all_url_lst


def crawler_baidu_by_keyword(keyword):
    """
    根据关键词抓取百度搜索结果
    :param keyword:
    :return: list 返回搜索结果的链接
    """
    # 关键词-->网站源码-->利用函数extract_links(html)获得链接

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0', # 缓存控制
        'Connection': 'keep-alive',
        'referer': quote('http://www.baidu.com/s?wd=python&pn=10'),
        'Host': 'www.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }

    all_link_lst = []
    url = 'https://www.baidu.com/s'
    for i in range(crawler_config.BD_CRAWLER_PAGE):
        params = {
            'wd': keyword,
            'pn': 10*i
        }

        session = requests.session()  # 保持会话
        res = session.get(url, params=params, headers=headers, allow_redirects=False)
        # session.get()的作用是去数据库查询数据并返回一个真实的对象，allow_redirects=False阻止302跳转
        time.sleep(crawler_config.SLEEP_TIME)
        res.encoding = 'utf-8'  # 对网页内容进行编码，否则中文无法正常显示（百度网页编码不是utf-8）
        link_lst = extract_links(res.text) # res.text 获得res的值，即网站源码
        all_link_lst.extend(link_lst)

    return all_link_lst


def extract_links(html):
    """
    从网页源码里解析出搜索结果的链接
    :param html:
    :return:
    """
    url_lst = []
    tree = etree.HTML(html)
    a_lst = tree.xpath("//div[@class='result c-container ']/h3/a[@data-click]")
    for a in a_lst:
        url_lst.append(a.attrib['href'])

    url_lst = [get_real_link(url) for url in url_lst]
    return url_lst

def get_real_link(url):
    """
    由源码获得真实的链接地址
    :param url:
    :return:
    """
    res = requests.get(url,allow_redirects=False)

    return res.headers['Location']


def test_extract_links():
    with open("../baidu.txt")as f:
        print(extract_links(f.read()))


def test_crawler_baidu_by_keyword():
    lst = crawler_baidu_by_keyword('python 教程')
    print(lst)


if __name__ == '__main__':
    run()
