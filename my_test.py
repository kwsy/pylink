import requests

# ----新浪首页爬取
# url = 'https://www.sina.com.cn/'
# res = requests.get(url)
# print(res.text)
# print(res.content.decode())

#---- 实现任意贴吧的爬虫，保存网页到本地

def crawl_badiu_tieba(keyword):

    url = "https://tieba.baidu.com/f"
    params = {
        "ie": "utf-8",
        "kw": f"{keyword}"
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'referer': quote('http://www.baidu.com/s?wd=python&pn=10'),
        # 'Host': 'www.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    response = requests.get(url, params=params, headers=headers)
    return response


if __name__ == '__main__':
    res = crawl_badiu_tieba('李毅')
    print(res.url)