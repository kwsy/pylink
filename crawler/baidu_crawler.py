import requests
import time
from lxml import etree
from urllib.parse import quote
from conf import crawler_config
from conf.bd_keywords import keyword_lst
from db.redis_client import r
def run():
    '''
    爬虫启动脚本
    :return:网址链接
    '''
    url_lst = crawler_all_keywords(keyword_lst) #
    #把url_lst列表中的内容写入到wlxfen_url_queue队列中，队列怎么创建呢？
    for i in range(len(url_lst)):
        r.lpush('wlxfen_url_queue', url_lst[i])

def crawler_all_keywords(keyword_list):
    '''
    爬取所有关键词的网址链接
    :param keyword_list: 所有关键词的列表
    :return: 没一个关键词对应的网址链接列表
    '''
    all_url_lst=[]
    for kd in keyword_list:
        lst=crawler_baidu_by_keyword(kd)
        all_url_lst.extend(lst)

    return all_url_lst


def crawler_baidu_by_keyword(keyword):
    """
    根据关键词抓取百度搜索结果
    :param keyword:
    :return: list 返回搜索结果的连接
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'referer': quote('http://www.baidu.com/s?wd=python&pn=10'),
        'Host': 'www.baidu.com',
        'User-Agent':  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    '''http头字段，web服务器通过user-agent进行来源审查'''
    all_link_lst=[]
    url = 'https://www.baidu.com/s'

    session = requests.session()
    for i in range(crawler_config.BD_MAX_CRAWLER_PAGE):
        params = {
                'wd': keyword,
                'pn': 10*i
            }

        res = session.get(url, params=params, headers=headers)#
        print(res.url)#测试params字段功能。在url链接后面补充新的字典内容。
        time.sleep(crawler_config.SLEEP_TIME)
        res.encoding = 'utf-8'  # 对网页内容进行编码,否则中文无法正常显示
        link_lst = extract_links(res.text)
        all_link_lst.extend(link_lst) #在列表末尾追加可迭代对象（元组，字符串，列表，字典）


    return all_link_lst


def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html:
    :return:
    """
    url_lst = []
    tree = etree.HTML(html)
    a_lst = tree.xpath("//div[@class='result c-container ']/h3/a[@data-click]")

    for a in a_lst:
        url_lst.append(a.attrib['href'])
    url_lst=[get_real_link(url) for url in url_lst]
    return url_lst


def test_extract_links():
    with open("../baidu.txt",'rb')as f:
        print(extract_links(f.read()))


def test_crawler_baidu_by_keyword():
    lst = crawler_baidu_by_keyword('python 教程')
    print(lst)

def get_real_link(url):
    '''
    获得真实的链接地址
    :param url:
    :return:
    '''
    res = requests.get(url,allow_redirects =False)
    return res.headers['Location']



if __name__ == '__main__':
    # test_extract_links()
    # url = 'http://www.baidu.com/link?url=LzQCUqcFg9l7-w4pu86rYjgudDCyhQ2RR-nW65NLhXOLq_MFHc7XaSeoct2KVQKdipQ48ZuXYIPNvlVtXjznRq'
    # get_real_link(url)
    run()
