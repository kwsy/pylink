import os
import time
import requests
from lxml import etree
from urllib.parse import quote


def extract_links_test(filepath):
    """
    测试函数，从文件中读取html，测试url获取是否正确
    从文件里读取html解析出搜索结果的连接
    :param filepath:文件路径
    :return:
    """
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    tree = etree.HTML(html)

    url_list = tree.xpath("//div[@class='result c-container ']/h3/a/@href")
    print(url_list)


def create_folder_htmlfile(path):
    if os.path.exists(path):
        print("{0}文件夹已存在，直接写入".format(path))
    else:
        os.mkdir(path)
        print("{0}文件夹不存在，新建成功".format(path))


def save_htmlfile(path_folder, keyword, num, html):
    create_folder_htmlfile(path_folder)

    keyword_folder = path_folder + "/" + keyword
    create_folder_htmlfile(keyword_folder)

    filename = "{0}/百度搜索第{1}页html内容_{2}".format(keyword_folder, num, keyword)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)


def generate_params(keyword, num):
    # 根据关键字生成字典params，用于sesion请求,pn根据页码数(n)变化，对应值为(n-1)*10
    params = {
        'wd': keyword,
        'pn': num * 10
    }
    print("params:{}".format(params))

    return params


''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''


def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html:
    :return:
    """
    tree = etree.HTML(html)

    url_list = tree.xpath("//div[@class='result c-container ']/h3/a/@href")
    return url_list


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

    session = requests.session()

    # 根据查询页数进行查询
    for tempnum_page in range(global_totalnum_page):

        # 生成params参数
        params = generate_params(keyword, tempnum_page)

        res = session.get(global_baidu_url, params=params, headers=headers, allow_redirects=False)
        res.encoding = 'utf-8'
        time.sleep(global_sleeptime)

        # 异常判断处理机制
        print(res.status_code)
        print(res.text)

        # 保存html文件到指定文件夹global_path_htmlfile，文件名举例：关键词python教程百度搜索第1页html内容
        if global_save_htmlfileflag == 1:
            save_htmlfile(global_path_htmlfile, keyword, (tempnum_page + 1), res.text)

        # 对每个html页面分析，获取所有的url，添加到列表url_list
        url_list = extract_links(res.text)

        url_total_list.extend(url_list)

        print("url_total_list包含{}组链接".format(len(url_total_list)))
        print(url_total_list)


if __name__ == '__main__':
    # 全局变量定义
    global_path_htmlfile = "./htmlfile"  # html存储文件夹
    global_save_htmlfileflag = 1

    global_keyword = "c语言教程"
    global_totalnum_page = 3
    global_baidu_url = 'https://www.baidu.com/s'

    global_sleeptime = 1

    url_total_list = []
    crawler_baidu_by_keyword(global_keyword)







