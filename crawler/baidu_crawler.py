import requests


def crawler_for_bd(keyword):
    """
    根据搜索关键词,利用百度进行搜索, 暂时不考虑分页, 只把第一页的结果抓取下来并分析出结果即可
    :param keyword:搜索关键词
    :return: 返回一个列表,列表里是搜索到的网站连接
    """


if __file__ == '__main__':
    lst = crawler_for_bd('python 教程')
    print(lst)