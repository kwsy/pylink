import requests
import time
from lxml import etree
from urllib.parse import quote
from  conf import bd_keywords  #调用conf模块里的bd_keywords.py，用bd_keywords.bd_keywords来获取列表



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
    lst.extend(link_lst)#extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）。

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

def find_all_keywords_url(l):
    """
        从bd_keywords.py中读取列表的关键词，然后将每个关键词爬取到的网页保存到keyword.txt
        :param :关键词列表 l
        :return:检索结果写入keyword.txt文件
        """
    d = {}
    for i in range(len(l)):
        lst = crawler_baidu_by_keyword(l[i])
        d[l[i]] = lst

    with open('..\keyword.txt', 'w') as kwd_file:
        for k, v in d.items():
            kwd_file.write(str(k) + ' ' + str(d[k]) + '\n')

def next_page(keyword):
    '''
    判断当输入python 教程关键词以后，是否有下一页标签。如果有，则解析这个网页的连接，返回下一页的网页连接；
    如果没有，则返回null
    :param 关键词列表
    :return:
     #输入关键词，获得页面网址，然后在页面上解析源码标签，看是否有下一页的标签
    '''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'referer': quote('http://www.baidu.com/s?wd=python&pn=10'),
        'Host': 'www.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    url = 'https://www.baidu.com/s'
    session = requests.session()

    params = {
            'wd': keyword,  # url链接参数wd查询关键字 (word) 一般以也会是一串字符
            'pn': 0  # url链接参数pn显示结果页数默认为0 其他每页递增rn
        }
    res = session.get(url, params=params, headers=headers, allow_redirects=False)


    tree = etree.HTML(res.text)

    li_nodes_1 = tree.xpath("//div[@id='page']/a[10]")[0]
    print(li_nodes_1.text)
    return li_nodes_1.text








if __name__ == '__main__':
    current_page = 1
    while next_page(bd_keywords.bd_keywords):
        current_page = current_page + 1

        if current_page > 10:
            break

    # with open("../baidu.txt",'rb')as f:
     #     print(extract_links(f.read()))
    find_all_keywords_url(bd_keywords.bd_keywords)



