from urllib import parse

def get_netloc(url):
    """
    解析url网址,获得网站的主页, 输入 http://www.coolpython.net/python_primary/data_type/bin_int_hex_oct.html
    返回http://www.coolpython.net
    :param url:
    :return:
    """
    url_split = parse.urlparse(url)
    urlparse = url_split[0]+'://'+url_split[1]
    return urlparse


if __name__ == '__main__':
    url = 'http://www.coolpython.net/python_primary/data_type/bin_int_hex_oct.html'
    netloc = get_netloc(url)
    print(url)
    print(netloc)
    net_loc2 = get_netloc('http://www.baidu.com/link?url=YBBxUxXC5vtVQcqrAi5xq4sk8meen3kjOVWh0MWgbi1WGqZhCZOaqzjj9BKVKbvkebowDvR9y32QlABZEL731a')
    print(net_loc2)
    pass