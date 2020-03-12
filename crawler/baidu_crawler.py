import requests
from lxml import etree
from urllib.parse import quote
import time
from conf.bd_keywords import keyword_lst
from conf.bd_crawler_config import PAGE_NUMBER, CRAWLER_SLEEP_TIME
from crawler.dispatch_worker import dispatch_url


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
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    url = 'https://www.baidu.com/s'
    session = requests.session()
    link_lst = []
    for i in range(PAGE_NUMBER):
        params = {
                    'wd': keyword,
                    'pn': 10*i
                }

        res = session.get(url, params=params, headers=headers)
        time.sleep(CRAWLER_SLEEP_TIME)
        res.encoding = 'utf-8'  # 对网页内容进行编码,否则中文无法正常显示
        link_lst += extract_links(res.text)  # 老师用ｅｘｔｅｎｄ

    real_link_lst = [get_real_link(link) for link in link_lst]
    return real_link_lst



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

    return url_lst


def get_real_link(url):
    res = requests.get(url, allow_redirects=False)
    return res.headers['Location']


def crawl_baidu_all_keyword(word_lst):
    all_keyeowrd_link_lst = []
    for word in word_lst:
        all_keyeowrd_link_lst.extend(crawler_baidu_by_keyword(word))

    return all_keyeowrd_link_lst


def run():
    lst = crawl_baidu_all_keyword(keyword_lst)
    print(lst)
    # with open("../data/百度urllist.txt", 'w') as f:
    #     for url in lst:
    #         f.write(url)
    #         f.write('\n')


def test_crawl_baidu_all_keyword():
    lst = crawl_baidu_all_keyword(keyword_lst)
    print(lst)
    print(len(lst))


def test_get_real_link():
    real_url = get_real_link("http://www.baidu.com/link?url=unijmehnccFkijNZ4YUZKQ4dUrDXMEGUagkxI-9UhdIpitQ39jNW9BBvr3Bie-ScYQYOfksl6A4ahFApjlyuKK")
    print(real_url)


def test_extract_links():
    with open("../baidu.txt")as f:
        print(extract_links(f.read()))


def test_crawler_baidu_by_keyword():
    lst = crawler_baidu_by_keyword('python 教程')
    print(lst)
    print(len(lst))


if __name__ == '__main__':
    # test_crawler_baidu_by_keyword()
    # test_get_real_link()
    # test_crawl_baidu_all_keyword()
    run()