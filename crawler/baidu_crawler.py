import requests
from conf.bd_keywords import key_word_list
import time
from lxml import etree
from urllib.parse import quote


def crawler_baidu_by_keyword(keyword=None):
    """
    根据关键词抓取百度搜索结果
    :param keyword:
    :return: list 返回搜索结果的连接
    """
    url = "https://www.baidu.com/s"
    params = {
        'wd': f'{keyword}',
        'pn': '0'
    }

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
    proxies = {'http': 'http://60.169.124.242:46301'}
    session = requests.session()
    response_data = session.get(url, headers=headers, params=params, proxies=proxies, allow_redirects=False)

    return response_data


def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html:
    :return:
    """
    tree = etree.HTML(html)
    a_lst = tree.xpath("//div[@class='result c-container ']/h3/a[@data-click]")
    link_lst = []
    for a in a_lst:
        link_lst.append(a.attrib['href'])
    return link_lst


if __name__ == '__main__':
    with open("../baidu.txt", encoding='utf-8') as f:
        print(extract_links(f.read()))
    # data = crawler_baidu_by_keyword(key_word_list[0])
    # print(data.content.decode('utf-8'))
    # with open("mybaidu.txt", 'w', encoding='utf-8') as f:
    #     f.write(data.content.decode())
    # time.sleep(2)
