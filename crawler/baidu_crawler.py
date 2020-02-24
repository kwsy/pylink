import requests
from urllib.parse import quote  # URL只允许一部分ASCII字符，其他字符（如汉字）是不符合标准的，此时就要进行编码


def crawler_baidu_by_keyword(keyword):
    """
    根据关键词抓取百度搜索结果
    :param keyword:
    :return: list 返回搜索结果的连接
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress,utf-8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'referer': quote('http://www.baidu.com/s?wd=python&pn=10'),
        'Host': 'www.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    url = 'https://www.baidu.com/s'
    params = {
        'wd': 'keyword',
        'pn': 0
    }
    session = requests.session() # 跨请求，保持某些参数
    res = session.get(url, params=params, headers=headers, allow_redirects=False)
    res.encoding = 'utf-8'
    url_lst = extract_links(res.text)
    return url_lst


def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html:
    :return:
    """
    return []

if __name__ == '__main__':
    lst = crawler_baidu_by_keyword('python 教程')
    print(lst)

    # with open("../baidu.txt")as f:
    #     extract_links(f.read())