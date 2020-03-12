from urllib.parse import urlparse


def get_url_netloc(url):
    return urlparse(url).netloc

def get_netloc(url):
    """
    解析url网址,获得网站的主页, 输入 http://www.coolpython.net/python_primary/data_type/bin_int_hex_oct.html
    返回http://www.coolpython.net
    :param url:
    :return:
    """
    result = urlparse(url)
    return result.scheme + "://" + result.netloc


if __name__ == '__main__':
    url_sample = 'https://www.csdn.net/gather_4a/MtTaEgzsNi1lZHUO0O0O.html'
    netloc = get_netloc(url_sample)
    print(netloc)