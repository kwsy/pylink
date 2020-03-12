import requests
from lxml import etree


def crawler_zhihu_zhuanlan(url):
    headers = {
            # "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            # "accept-encoding": "gzip, deflate, br",
            # "accept-language": "zh-CN,zh;q=0.9",
            # "cache-control": "max-age=0",
            # "sec-fetch-mode": "navigate",
            # "sec-fetch-site": "none",
            # "sec-fetch-user": "?1",
            # "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
               }
    # url = url
    session = requests.session()
    res = session.get(url, headers=headers)
    return res.content.decode("utf-8")


def exact_zhuanlan_info(html):
    tree = etree.HTML(html)

def test_exact_zhuanlan_info():
    with open('../zhihu.txt', encoding='utf-8') as f:
        html = f.read()
    print(html)


def test_get_zhuanlan_info():
    res = crawler_zhihu_zhuanlan("https://zhuanlan.zhihu.com/c_174409057")
    print(res)


if __name__ == '__main__':
    test_exact_zhuanlan_info()
