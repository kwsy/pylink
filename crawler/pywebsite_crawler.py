from common.url_utils import url_to_html
from lxml import etree
import os


lst_miss_match = []  # 未匹配成功网站
judge_dict_score = {"python": 4, "教程": 1, "数据分析": 2, "人工智能": 1, "大数据": 1}  # 利用关键字相关性判断Python分值


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

    tree = etree.HTML(html)
    score = 0
    tree_path = {'keyword': '//meta[@name = "keywords"]', 'description': '//meta[@name = "description"]'}  # xpath专用路径
    for key in tree_path:
        score += _judge_by_py_keyword_ex(tree, tree_path[key])
    if score >= 5:
        return True
    else:
        return False


def _judge_by_py_keyword_ex(tree, xpath_name):
    """
    提供xpath路径接口,判断网页关键信息是否为有效分值
    :param xpath_name:
    :param tree:
    :return:
    """
    score = 0
    nodes_lst = tree.xpath(xpath_name)
    if nodes_lst:
        node = nodes_lst[0]
        node_content = node.attrib['content'].lower()

        for key in judge_dict_score:
            if node_content.find(key) != -1:
                score += judge_dict_score[key]
    return score


def judge_by_py_meau(html):
    """
    提取菜单关键信息，来判断是否是python主题网站
    :return:
    """
    tree = etree.HTML(html)
    a_lst = tree.xpath('//li/a')    # 获取标签部分
    print(a_lst)
    score = 0
    if a_lst:
        try:
            node_text_lst = [node.text.lower() for node in a_lst if 1 < len(node.text) <= 10]
            print(node_text_lst)
            for node_text in node_text_lst:
                for key in judge_dict_score:
                    if node_text.find(key) != -1:
                        score += judge_dict_score[key]
        except Exception as e:
            print(e)
    if score >= 5:
        return True
    else:
        return False


def save_miss_lst(lst_miss_match):
    """无法识别部分写入对应文档，人工查阅"""
    if os.path.exists("../data/miss_match_url/lst_miss_match.txt"):
        print("lst_miss_match文件已存在，直接写入")
    else:
        os.mkdir("../data/miss_match_url/lst_miss_match.txt")
        print("lst_miss_match文件不存在，新建成功")

    with open("../data/miss_match_url/lst_miss_match.txt", 'a', encoding='utf-8') as f:
        for single_url in lst_miss_match:
            f.write(single_url + "\n")


def run():
    """
    执行程序：url转html→解析html→判断关键信息→根据分值判断True→返回False部分加入到miss_lst后期人工判断
    :return:
    """
    # url = 'https://www.runoob.com/python3/python3-tutorial.html'
    # url = 'https://www.itcodemonkey.com'
    # url = 'http://www.kidscode.cn/python'
    url = 'https://www.bilibili.com/'
    if judge_py_website(url):

    else:
        save_miss_lst(lst_miss_match)


if __name__ == '__main__':
    run()

