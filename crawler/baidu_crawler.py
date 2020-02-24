import os
import time
import requests
from lxml import etree
from urllib.parse import quote

from conf.bd_keywords import keywords
from common.url_utils import get_netloc

#测试用，从制定文件文件读取html，采用etree从中获取需要的url
def extract_links_test(filename):
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

#判断指定路径是否存在，无则创建
def create_folder_htmlfile(path):
    if os.path.exists(path):
        print("{0}文件夹已存在，直接写入".format(path))
    else:
        os.mkdir(path)
        print("{0}文件夹不存在，新建成功".format(path))

#保存html至以爬虫关键字及页码命名的文件
def save_htmlfile(path_folder, keyword, num, html):
    create_folder_htmlfile(path_folder)

    keyword_folder = path_folder + "/" + keyword
    create_folder_htmlfile(keyword_folder)

    filename = "{0}/百度搜索第{1}页html内容_{2}".format(keyword_folder, num, keyword)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

#保存url列表至以爬虫关键字命名的文件
def save_urlfile(path_folder, keyword, url_list):
    create_folder_htmlfile(path_folder)

    keyword_folder = path_folder + "/" + keyword
    create_folder_htmlfile(keyword_folder)

    filename = "{0}/百度搜索分析url内容_{1}".format(keyword_folder, keyword)
    with open(filename, 'w', encoding='utf-8') as f:
        for str_url in url_list:
            f.write(str_url)
            f.write("\n")


#根据关键字及爬取页面数，生成字典，用于session请求
def generate_params(keyword, num):
    # 根据关键字生成字典params，用于sesion请求,pn根据页码数(n)变化，对应值为(n-1)*10
    params = {
        'wd': keyword,
        'pn': num * 10
    }
    print("params:{}".format(params))

    return params


# 将百度链接转化为真实链接，并得到主页
def url_baidu_to_realmain(url):
    res = requests.get(url, allow_redirects=False)
    real_url = res.headers['location']
    #得到真实主页链接，都是平台，需要针对性处理
    #realmain_url = get_netloc(real_url)
    #return realmain_url

    #得到真是链接
    return real_url

#将百度链接列表转化为真实链接列表
def urlist_baidu_to_realmain(url_list):
    realmain_url_list=[]
    print(url_list)
    for url in url_list:
        print(url)
        realmain_url = url_baidu_to_realmain(url)
        #print("Real_url")
        #print(realmain_url)
        realmain_url_list.append(realmain_url)
        #print("Real_url_list")
        #print(realmain_url_list)
    return realmain_url_list

#根据html，获取真实链接列表
def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html:
    :return:
    """
    tree = etree.HTML(html)
    #得到网址列表
    url_list = tree.xpath("//div[@class='result c-container ']/h3/a/@href")
    #将网址列表（百度）生成真实列表
    real_url_list = urlist_baidu_to_realmain(url_list)
    return real_url_list


#根据单个关键字爬取，返回有效url
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

        url_keyword_list.extend(url_list)
        print("url_total_list包含{}组链接".format(len(url_keyword_list)))
        print(url_keyword_list)
    #返回单个关键字所有页码关键字url清单
    return url_keyword_list

#根据所有关键字爬取，返回有效url
def crawler_baidu_by_all_keyword(keywords):
    url_all_keywords_list_temp=[]
    for keyword in keywords:
        url_keyword_list = crawler_baidu_by_keyword(keyword)
        print("百度爬取关键字完毕_{0}".format(keyword))

        #保存单个关键字获取的url地址
        save_urlfile(global_path_urlfile, keyword, url_keyword_list)

        #将所有关键字的url整合到url_all_keywords_list_temp中
        url_all_keywords_list_temp.extend(url_keyword_list)

    #url地址去重
    url_all_keywords_list = list(set(url_all_keywords_list_temp))
    #保存所有关键字的url地址
    save_urlfile(global_path_urlfile, "汇总", url_all_keywords_list)





if __name__ == '__main__':
    # 全局变量定义
    global_path_htmlfile = "./htmlfile"  # html存储文件夹
    global_save_htmlfileflag = 1

    global_path_urlfile = "./urlfile" # url存储文件夹

    global_keyword = "c语言教程"
    global_totalnum_page = 3
    global_baidu_url = 'https://www.baidu.com/s'


    global_sleeptime = 1

    url_keyword_list = []
    url_all_keywords_list = []
    #crawler_baidu_by_keyword(global_keyword)

    print(keywords)
    crawler_baidu_by_all_keyword(keywords)





