from urllib.parse import urlparse
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

if __name__ == '__main__':
    url = 'http://www.coolpython.net/python_primary/data_type/bin_int_hex_oct.html'
    netloc = get_netloc(url)
    print(url)