def crawler_baidu_by_keyword(keyword):
    """
    根据关键词抓取百度搜索结果
    :param keyword:
    :return: list 返回搜索结果的连接
    """

def extract_links(html):
    """
    从网页源码里解析出搜索结果的连接
    :param html:
    :return:
    """


if __name__ == '__main__':
    # lst = crawler_baidu_by_keyword('python 教程')
    # print(lst)

    with open("../baidu.txt")as f:
        extract_links(f.read())