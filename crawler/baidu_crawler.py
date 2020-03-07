import requests
import time
from lxml import etree
from urllib.parse import quote


def crawler_baidu_by_keyword(keyword):
    """
    根据关键词抓取百度搜索结果
    :param keyword:
    :return: list 返回搜索结果的连接
    """
    lst = []
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'referer': quote('http://www.baidu.com/s?wd=python&pn=10'),
        'Host': 'www.baidu.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    url ='https://www.baidu.com/s'
    session = requests.session()

    for i in range(5):
        params = {
            'wd': keyword,
            'pn':  i*10
                 }
        res = session.get(url, params=params, headers=headers,allow_redirects=False)
        res.encoding = 'utf-8'
        time.sleep(3)

        link_lst = extract_links(res.text)
        lst.extend(link_lst)

    return lst

def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html:
    :return:
    """
    url_lst=[]
    tree = etree.HTML(html)
    a_nodes=tree.xpath("//div[@class='result c-container ']/h3/a[@data-click]")

    for a in a_nodes:
        url_lst.append(a.attrib['href'])
    return url_lst





if __name__ == '__main__':
     # with open("../baidu.txt",'rb')as f:
     #     print(extract_links(f.read()))

     lst = crawler_baidu_by_keyword('python 教程')
     print(len(lst))

