def judge_py_website(url):
    """
    判断url是一个与python非常相关的网站
    :param url:
    :return:
    """
    tree = etree.HTML(html)

if __name__ == '__main__':
    url = 'http://www.kidscode.cn/python'
    print(judge_py_website(url))