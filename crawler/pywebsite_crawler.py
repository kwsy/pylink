from common.url_utils import url_to_html
from lxml import etree


lst_miss_match = []     # 未匹配成功网站
tree_path = {"keyword": '//meta[@name = "keywords"]', "description": '//meta[@name = "description"]'}

def judge_py_website(url):
    """
    判断url是一个与python非常相关的网站,做判断函数使用
    :param url:
    :return:
    """
    html = url_to_html(url)

    if judge_by_py_keyword(html):
        return True
    elif judge_by_py_meau(html):
        return True
    else:
        global lst_miss_match
        lst_miss_match.append(url)
        return False


def judge_by_py_keyword(html):
    """
    提取网页关键词，来判断是否是python主题网站
    :return:
    """
    tree_path = {"keyword": '//meta[@name = "keywords"]', "description": '//meta[@name = "description"]'}
    tree = etree.HTML(html)
    keywords_lst = tree.xpath('//meta[@name = "keywords"]')
    if keywords_lst:
        keyword = keywords_lst[0]
        content = keyword.attrib['content'].lower()
        print(content)
        if content.find("python") != -1 and content.find("教程") != -1:
            pass
    description_lst = tree.xpath('//meta[@name = "description"]')
    if description_lst:
        description = description_lst[0]
        content2 = description.attrib['content'].lower()
        print(content2)
        if content2.find("python") != -1 and content2.find("教程") != -1:


def judge_by_py_meau(html):
    """
    提取菜单关键信息，来判断是否是python主题网站
    :return:
    """
    pass

def run():
    """
    执行程序：url→html→解析html→判断关键信息→返回True or False
    :return:
    """
    #url = 'https://www.runoob.com/python3/python3-tutorial.html'
    url = 'http://www.kidscode.cn/python'
    html_info = judge_py_website(url)
    return html_info


if __name__ == '__main__':
    url = 'http://www.kidscode.cn/python'
    print(judge_py_website(url))