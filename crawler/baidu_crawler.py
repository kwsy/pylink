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

    for i in range(5):      #通过for 循环实现连续5页的网页链接抓取
        params = {
            'wd': keyword,  #url链接参数wd查询关键字 (word) 一般以也会是一串字符
            'pn':  i*10     #url链接参数pn显示结果页数默认为0 其他每页递增rn
                 }
        res = session.get(url, params=params, headers=headers,allow_redirects=False)
        res.encoding = 'utf-8'  #用url编码方式进行解码你才能看到真实的内容
        time.sleep(3)           #函数推迟调用线程的运行，可通过参数secs指秒数，表示进程挂起的时间

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

