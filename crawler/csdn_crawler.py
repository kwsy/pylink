import requests
from lxml import etree
from urllib.parse import quote
from common.url_utils import url_to_html


def get_blogger_info(url):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    :param url:csdn.net为主信息
    :return:
    """
    html = url_to_html(url)





if __name__ == '__main__':
    url = 'https://blog.csdn.net/KWSY2008'
    #print(get_blogger_info)
    with open('../csdn.txt',)