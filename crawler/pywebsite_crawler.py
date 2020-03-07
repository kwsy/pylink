import re
import requests
from lxml import etree

def get_html_from_url(url):
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
    response = requests.get(url, headers=headers)
    return response.text

def get_infolist_from_html_byxpath(html, string_xpath):
    tree = etree.HTML(html)
    keyinfolist = tree.xpath(string_xpath)
    return keyinfolist

def get_describe_content_dict(html):
    describe_content_dict = {}

    tree = etree.HTML(html)
    content_description = tree.xpath("//meta[@name='description']/@content")
    content_keywords = tree.xpath("//meta[@name='keywords']/@content")

    if len(content_description) != 0:
        describe_content_dict["description"] = content_description[0]
    else:
        print("无description信息")

    if len(content_keywords) != 0:
        describe_content_dict["keywords"] = content_keywords[0]
    else:
        print("无keywords信息")

    return describe_content_dict

def judge_list_inlucde_keyword(describe_content_dict, keyword):
    pattern = re.compile(keyword, re.I)              # 匹配忽略大小写
    for content in describe_content_dict.values():
        if content.find(keyword) != -1:
            return True
        res = pattern.findall(content)
        if len(res) != 0:
            return True
    return False

def judge_py_website(url):
    """
    判断url是一个与python非常相关的网站
    :param url:
    :return:
    """
    keyword = "Python"
    html = get_html_from_url(url)                                                   # 从url获取html
    describe_content_dict = get_describe_content_dict(html)                         # 从html获取描述信息，返回字典形式
    flag_have_keyword = judge_list_inlucde_keyword(describe_content_dict, keyword)  # 从字典中判断是否有关键词python(无论大小写)
    return flag_have_keyword

if __name__ == '__main__':
    url = 'http://www.kidscode.cn/python'
    # url = 'https://zhuanlan.zhihu.com/c_1099248962871169024'
    # url = 'https://zhuanlan.zhihu.com/p/109450078'
    result_judge_python = judge_py_website(url)
    print("result_judge_python:{}".format(result_judge_python))


