import requests
from lxml import etree

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

url = 'https://www.w3cschool.cn/python3'
res = requests.get(url, headers=headers)
res.encoding = 'utf-8'

tree = etree.HTML(res.text)
keywords = tree.xpath('//meta[@name="keywords"]')
print(keywords)

