import re
import time
import requests
from common.url_utils import get_netloc
from lxml import etree
from conf import redis_conf
from conf import mongo_conf
from db import redis_client
from db import mongo_client

# def get_describe_content_dict(html):
#     describe_content_dict = {}
#
#     tree = etree.HTML(html)
#     content_description = tree.xpath("//meta[@name='description']/@content")
#     content_keywords = tree.xpath("//meta[@name='keywords']/@content")
#
#     if len(content_description) != 0:
#         describe_content_dict["description"] = content_description[0]
#     else:
#         print("无description信息")
#
#     if len(content_keywords) != 0:
#         describe_content_dict["keywords"] = content_keywords[0]
#     else:
#         print("无keywords信息")
#
#     return describe_content_dict

# def judge_list_inlucde_keyword(describe_content_dict, keyword):
#     pattern = re.compile(keyword, re.I)              # 匹配忽略大小写
#     for content in describe_content_dict.values():
#         if content.find(keyword) != -1:
#             return True
#         res = pattern.findall(content)
#         if len(res) != 0:
#             return True
#     return False

# def judge_py_website(url):
#     """
#     判断url是一个与python非常相关的网站
#     :param url:
#     :return:
#     """
#     keyword = "Python"
#     html = get_html_from_url(url)                                                   # 从url获取html
#     describe_content_dict = get_describe_content_dict(html)                         # 从html获取描述信息，返回字典形式
#     flag_have_keyword = judge_list_inlucde_keyword(describe_content_dict, keyword)  # 从字典中判断是否有关键词python(无论大小写)
#     return flag_have_keyword

# if __name__ == '__main__':
#     url = 'http://www.kidscode.cn/python'
#     # url = 'https://zhuanlan.zhihu.com/c_1099248962871169024'
#     # url = 'https://zhuanlan.zhihu.com/p/109450078'
#     result_judge_python = judge_py_website(url)
#     print("result_judge_python:{}".format(result_judge_python))

def Jduge_in_urlbacklist(url, list_urlbacklist):
    #转换结果
    for i in list_urlbacklist:
        print(i)
        # if url in urlback:
    #     if url.find("urlback") != -1:
    #         return True
    # return False


def get_html_from_url(session,url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        "content-type": "text/html; charset=utf-8",
        # 'referer': quote('http://www.baidu.com/s?wd=python&pn=10'),
        # 'Host': 'https://zhuanlan.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }
    time.sleep(3)
    response = session.get(url, headers=headers, allow_redirects=False)
    response.encoding = "utf-8"
    return response.text


def Jduge_html_keyword_include(tree, name_meta):
    list_meta = tree.xpath("//meta[@name='{}']".format(name_meta))

    if list_meta:
        str_description = list_meta[0].attrib['content'].lower()
        print(name_meta, str_description)
        if str_description.find("python") != -1 and str_description.find("教程") != -1:
            print("关键字满足条件")
            return True
    return False

def Jduge_html_by_button(tree):
    list_a = tree.xpath("//li//a")
    if list_a:
        for node in list_a:
            if node.text.lower().find('python') != -1 and len(node.text) <10:
                return True
    return False

# 通过判断html总关键词keyword的数量是否大于num_satisfy，大于返回True，否则返回False
def get_keyword_totalnum(keyword,html,num_satisfy):

    pattern = re.compile(keyword, re.I)              # 匹配忽略大小写
    res = pattern.findall(html)

    if len(res) > num_satisfy:
        return True
    else:
        return False

def judge_py_website(url):
    # 黑名单 放到conf目录下配置
    list_urlbacklist = ('www.bjsxt.com',)
    num_satisfy = 10

    # netloc = get_netloc(url)
    # if netloc in list_urlbacklist:
    #     return False

    if Jduge_in_urlbacklist(url, list_urlbacklist) == True:
        print("url:{}为黑名单".format(url))
        return False

    session = requests.session()
    html = get_html_from_url(session, url)                                                   # 从url获取html
    tree = etree.HTML(html)
    print('tree')
    print(tree)
    if tree == None:
        return False
    # 判断html中有没有关键字description
    if Jduge_html_keyword_include(tree, "description") == True:
        print("description中包含python、课程")
        return True
    # 判断html中有没有关键字keywords
    if Jduge_html_keyword_include(tree, "keywords") == True:
        print("keywords中包含python、课程")
        return True
    if Jduge_html_by_button(tree) == True:
        print("菜单中包含python")
        return True
    # # 判断网页中python数量，大于一定数量判定是
    # if get_keyword_totalnum('python',html,num_satisfy) == True:
    #     print("python数量大于{}".format(num_satisfy))
    #     return True
    return False

def pywebsite_run():
    """
    从pywebsiteredis队列中依次读取url分析获取专栏列表
    :param url:
    :return:
    """
    # dict_pywebsite = {}
    while True:
        dict_pywebsite = {}
        url = redis_client.pop_queue(redis_conf.QueueConfig.py_website)
        print(url)
        if  url == None:
            time.sleep(10)
            continue
        if judge_py_website(url) == True:
            dict_pywebsite['属性'] = "个人网站"
            dict_pywebsite['url'] = url
            mongo_client.collection_insert_one_pywebsite(dict_pywebsite)
            for x in mongo_client.collection_pywebsite.find():
                print(x)

# 本部分还需优化
if __name__ == '__main__':
    url = 'http://www.kidscode.cn/python'
    url = 'https://www.itcodemonkey.com'
    # url = 'https://zhuanlan.zhihu.com/c_1099248962871169024'
    # url = 'https://zhuanlan.zhihu.com/p/109450078'
    pywebsite_run()
    # result = judge_py_website(url)
    # print(result)
