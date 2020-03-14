import os
import time
import requests
from lxml import etree
from functools import wraps
from urllib.parse import quote
from requests import exceptions
from conf.bd_keywords import keywords
from common.url_utils import get_netloc, HttpCodeException
from conf.crawler_config import *
from common.decorator import retry
from crawler.dispath_worker import dispath_url

CONTENT_NUM = 0     # 抓取数量

def extract_links_test(filename):
    """
    测试函数，从文件中读取html，测试url（搜索结果的连接）获取是否正确
    :param filename: 文件名称
    :return: url（搜索结果的连接）列表
    """
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    tree = etree.HTML(html)
    url_list = tree.xpath("//div[@class='result c-container ']/h3/a/@href")

    return url_list


def create_folder_htmlfile(path):
    """
    判断指定路径是否存在，无则创建
    :param path:
    :return:
    """
    if os.path.exists(path):
        print("{0}文件夹已存在，直接写入".format(path))
    else:
        os.mkdir(path)
        print("{0}文件夹不存在，新建成功".format(path))


def save_htmlfile(path_folder, keyword, num, html):
    """
    保存html至以爬虫关键字及页码命名的文件   "../data/htmlfile/python 教程/百度搜索第1页html内容_python 教程"
    :param path_folder:文件保存路径
    :param keyword:爬虫关键词
    :param num:搜索当前页码
    :param html:要保存的html信息
    :return:
    """
    create_folder_htmlfile(path_folder)
    keyword_folder = os.path.join(path_folder, keyword)
    create_folder_htmlfile(keyword_folder)

    filename = "{0}/百度搜索第{1}页html内容_{2}".format(keyword_folder, num, keyword)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)


def save_urlfile(path_folder, keyword, url_list):
    """
    保存url列表至以爬虫关键字命名的文件 "../data/urlfile/python 教程/百度搜索url内容_python 教程"
    :param path_folder:文件保存路径
    :param keyword:爬虫关键词
    :param url_list:要保存的url列表
    :return:
    """
    create_folder_htmlfile(path_folder)

    keyword_folder = os.path.join(path_folder, keyword)
    create_folder_htmlfile(keyword_folder)

    filename = "{0}/百度搜索分析url内容_{1}".format(keyword_folder, keyword)
    with open(filename, 'w', encoding='utf-8') as f:
        for str_url in url_list:
            f.write(str_url)
            f.write("\n")


def generate_params(keyword, num):
    """
    根据关键字生成字典params，用于sesion请求,pn根据页码数(n)变化，对应值为(n-1)*10
    :param keyword:爬虫关键词
    :param num:当前页码数
    :return:
    """
    return {'wd': keyword, 'pn': num * 10}


@retry(TIMES_REQUESTS_MAX, TIME_REQUEST_SLEEP)
def url_baidu_to_realmain(url):
    """
    将百度链接转化为真实链接，并得到主页
    :param url:要转换的链接
    :return:转换之后的真实链接
    """

    response = requests.get(url, allow_redirects=False)  # allow_redirects设置重定向,默认开启;
    real_url = response.headers['location']

    return real_url


def urlist_baidu_to_realmain(url_list):
    """
    将百度链接列表转化为真实链接列表
    :param url_list:百度链接列表
    :return:转换之后的真实链接列表
    """

    return [url_baidu_to_realmain(url) for url in url_list]


def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html: html信息
    :return: 搜索结果列表
    """
    tree = etree.HTML(html)
    # 得到网址列表
    url_list = tree.xpath("//div[@class='result c-container ']/h3/a/@href")

    # 将网址列表（百度）生成真实列表
    real_url_list = urlist_baidu_to_realmain(url_list)
    return real_url_list


@retry(TIMES_REQUESTS_MAX, TIME_REQUEST_SLEEP)
def params_request(session, url, params, headers):
    """
    获取session状态及html内容
    :param session: session参数
    :param url: 搜索引擎url
    :param params: url需要增加的键值对
    :param headers: 请求头
    :return: session请求状态及html内容
    """
    # 通过exceptions异常来判断请求是否成功

    response = session.get(url, params=params, headers=headers, allow_redirects=False)
    if response.status_code != 200:
        raise HttpCodeException
    return response.text


def crawler_baidu_by_keyword(keyword):
    """
    根据单个关键词抓取百度搜索结果
    :param keyword:
    :return: list 返回搜索结果的连接
    """
    list_url_onekeyword = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'referer': quote('http://www.baidu.com/s?wd=python&pn=10'),
        'Host': 'www.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    session = requests.session()
    for num_page in range(TOTALNUM_SEARCH_PAGE):  # 根据查询页数进行查询
        time.sleep(TIME_REQUEST_SLEEP)
        print("{0}关键词第{1}页".format(keyword, (num_page + 1)))
        params = generate_params(keyword, num_page)  # 获取搜索关键字
        html = params_request(session, URL_BAIDU, params, headers)

        if html is not None:
            url_list = extract_links(html)  # 获取单页有效链接列表

            list_url_onekeyword.extend(url_list)  # 更新单个关键字有效链接列表
            if FLAG_SAVE_HTMLFILE == 1:  # 根据配置参数保存html内容
                save_htmlfile(PATH_HTMLFILE, keyword, (num_page + 1), html)

    return list_url_onekeyword  # 返回单个关键字所有页码关键字url列表


def crawler_baidu_by_all_keyword(keywords):
    """
    根据所有关键字爬取，返回有效url
    :param keywords:搜索关键词
    :return: list 返回搜索结果的连接
    """
    lst_url_allword = []
    for keyword in keywords:
        lst_url_oneword = crawler_baidu_by_keyword(keyword)
        dispath_url(lst_url_oneword)
        global CONTENT_NUM
        CONTENT_NUM += len(lst_url_oneword)
        print(CONTENT_NUM)
        if FLAG_SAVE_URLFILE == 1:
            save_urlfile(PATH_URLFILE, keyword, lst_url_oneword)
        lst_url_allword.extend(lst_url_oneword)

    lst_url_allword = list(set(lst_url_allword))  # url地址去重

    if FLAG_SAVE_URLFILE == 1:
        save_urlfile(PATH_URLFILE, "url汇总", lst_url_allword)  # 保存所有关键字的url地址

    return lst_url_allword


def run():
    crawler_baidu_by_all_keyword(keywords)


def test_extract_links(html="../baidu.txt"):
    with open(html, encoding='utf-8') as f:
        print(extract_links(f.read()))


def test_crawler_baidu_by_keyword(keyword='python教程'):
    lst = crawler_baidu_by_keyword(keyword)
    print(lst)


if __name__ == '__main__':
    run(keywords)
