import requests
from lxml import etree
def crawler_baidu_by_keyword(keyword):
    """
    根据关键词抓取百度搜索结果
    :param keyword:
    :return: list 返回搜索结果的连接
    """

    headers ={
              'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
              'Accept - Encoding': 'gzip, deflate, br',
              'Accept - Language': 'zh-CN, zh;en-US;q=0.8,en;q=0.7',
              'Cache - Control': 'max-age = 0',
              'Connection': 'keep-alive',
              'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
             }

    url ='https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd='+keyword

    res =requests.get(url,headers=headers)
    print(res.text)
     # return lst

def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html:
    :return:
    """
    tree = etree.HTML(html)
    # print(etree.tostring(tree))
    body = tree.xpath('body')
    # print(body, type(body[0]))
    div_nodes = tree.xpath("//div")
    print(div_nodes)
    #
    # print(div0_1, type(div0_1))
    # print(div0_1 == div0_2)

if __name__ == '__main__':
    crawler_baidu_by_keyword('python 教程')
    # lst = crawler_baidu_by_keyword('python 教程')
    # print(lst)

    # with open("../baidu.txt",'rb')as f:
    #     extract_links(f.read())