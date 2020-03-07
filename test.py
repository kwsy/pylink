'''
假设修改这里会怎样
'''
import requests
import time
from urllib.parse import quote

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

url = 'https://www.baidu.com/s'

params = {
            'wd': 'python 教程',
            'pn': 0
        }

session = requests.session()

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").text


def get_baidu_data():
    print(params)
    res = session.get(url, params=params, headers=headers, allow_redirects=False)
    res.encoding = 'utf-8'
    print(res.status_code)

get_baidu_data()

