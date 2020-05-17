from urllib.parse import urlparse
import requests
from common.decorator import retry
from conf.crawler_config import TIMES_REQUESTS_MAX, TIME_REQUEST_SLEEP


class HttpCodeException(Exception):
    pass


def get_netloc(url):
    """
    解析url网址,获得网站的主页, 输入 http://www.coolpython.net/python_primary/data_type/bin_int_hex_oct.html
    返回http://www.coolpython.net
    :param url:
    :return:
    """
    result = urlparse(url)
    result_url = result.scheme + "://" + result.netloc
    return result_url

def url_to_html(url, params=None):
    """
    解析url网站获取html
    :param params:
    :param url:
    :return:html
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    session = requests.session()
    html = params_request(session, url, headers, params)

    return html


@retry(TIMES_REQUESTS_MAX, TIME_REQUEST_SLEEP)
def params_request(session, url, headers, params=None):
    """
    获取session状态及html内容
    :param url: 搜索引擎url
    :param session: session参数
    :param params: url需要增加的键值对
    :param headers: 请求头
    :return: session请求状态及html内容
    """
    # 通过exceptions异常来判断请求是否成功

    response = session.get(url, params=params, headers=headers, allow_redirects=False)
    print(response.status_code)
    if response.status_code != 200:
        raise HttpCodeException
    return response.text


if __name__ == '__main__':
    url = 'http://www.coolpython.net/python_primary/data_type/bin_int_hex_oct.html'
    netloc = get_netloc(url)
    print(netloc)
    print(url_to_html('https://zhuanlan.zhihu.com/c_1099248962871169024'))
