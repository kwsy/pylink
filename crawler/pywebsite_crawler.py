import os

from lxml import etree
from common.url_utils import url_to_html
from conf.mongo_conf1 import MongoCollection
from conf.redis_conf import QueueConfig
from crawler import run_crawler_worker
from db.mongo_client import mongo_drop_collect, mongo_find_collect, mongo_remove_one
from db.redis_client import lpush_queue
from datetime import datetime
import logging
from crawler import get_alexa_sort
from urllib.parse import urlparse
import sys
sys.path.append("../")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


lst_miss_match = []  # 未匹配成功网站
judge_dict_score = {"python": 4, "教程": 1, "数据分析": 2, "人工智能": 1, "大数据": 1}  # 利用关键字相关性判断Python分值


def judge_py_website(url):
    """
    判断url是一个与python非常相关的网站,做判断函数使用
    :param url:
    :return:
    """
    html = url_to_html(url)
    score = judge_by_py_keyword(html)[1] + judge_by_py_meau(html)[1]
    localtime = datetime.now()
    if score == 0:
        _remove_py_website_zero(url)    # 有点影响效率
    url_netloc = urlparse(url).netloc   # http://www.zhihu.com → www.zhihu.com
    rank = get_alexa_sort(url_netloc)
    if judge_by_py_keyword(html)[0]:
        return {"score": score, "href": url, "insert_time": localtime, "web_rank": rank}
    elif judge_by_py_meau(html)[0]:
        return {"score": score, "href": url, "insert_time": localtime, "web_rank": rank}
    else:
        lst_miss_match.append(url)
        save_miss_lst(lst_miss_match)


def _remove_py_website_zero(url):
    """该函数判断分数为0，移除mongo"""
    data = mongo_find_collect(MongoCollection.pywebsite_mongo, url)
    if data is not None:
        mongo_remove_one(MongoCollection.pywebsite_mongo, url)


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
        return True, score
    else:
        return False, 0


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
            print("judge_by_py_meau error", e)
    if score >= 5:
        return True, score
    else:
        return False, 0


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


def test():
    """
    测试专用
    :return:
    """
    # url = 'https://www.runoob.com/python3/python3-tutorial.html'
    # url = 'https://www.itcodemonkey.com'
    # url = 'http://www.kidscode.cn/python'
    lpush_queue(QueueConfig.pywebsite_queue, 'https://www.runoob.com/python3/python3-tutorial.html')
    mongo_drop_collect(MongoCollection.pywebsite_mongo)  # 清空表，正式时需删掉
    run()


def run():
    """
    执行程序：url转html→解析html→判断关键信息→根据分值判断True→返回False部分加入到miss_lst后期人工判断→非字典型无法加入mongo
    :return:
    """
    run_crawler_worker(QueueConfig.pywebsite_queue, MongoCollection.pywebsite_mongo, judge_py_website)


if __name__ == '__main__':
    #print(judge_py_website('http://www.kidscode.cn/python'))
    # test()
    mongo_drop_collect(MongoCollection.pywebsite_mongo)
    mongo_drop_collect(MongoCollection.csdn_mongo)
    mongo_drop_collect(MongoCollection.zhihu_mongo)