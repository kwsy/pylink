import requests
from lxml import etree


def get_alexa_sort(netloc):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    url = 'http://www.alexa.cn/' + netloc
    url = 'http://www.alexa.cn/rank/' + netloc
    res = requests.get(url, headers=headers)
    token_index = res.text.find('token')
    domain_index = res.text.find('domain', token_index)
    token = res.text[token_index + len("token : '"): domain_index - 3]

    domain_left = res.text.find("'", domain_index)
    domain_right = res.text.find("'", domain_left+1)
    domain = res.text[domain_left+1:domain_right]
    url = 'http://www.alexa.cn/api/alexa/free'

    params = {'token': token, 'url': netloc}
    res = requests.get(url, params, headers=headers)
    data = res.json()

    sort = data['data']['world_rank']
    if sort == 0:
        return 2**32 -1

    return sort


sort = get_alexa_sort('www.yuqiaochuang.com')
print(sort)
