import requests
from lxml import etree
from common.url_utils import url_to_html


def get_blogger_info(html):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    {week_rank':周排名, 'sum_rank':总排名, 'original':原创, 'fans_num':粉丝,
     'like_num':获赞, 'comment_num':评论,'visit_num':访客, 'blog_level':博客等级}
    :param html: csdn.net为主信息
    :return:
    """

    tree = etree.HTML(html)
    rank = tree.xpath('//div[@class="grade-box clearfix"]/dl[@title]/@title')
    information_num = tree.xpath('//div[@class = "data-info d-flex item-tiling"]/dl[@class = "text-center"]/@title')
    blog_level = \
    tree.xpath('//div[@class="grade-box clearfix"]/dl[@class = "aside-box-footerClassify"]/dd/a/@title')[0][0]  # 博客等级

    lst_info = rank + information_num + [blog_level]  # info形成列表
    lst_name = ['week_rank', 'sum_rank', 'original', 'fans_num', 'like_num', 'comment_num',
                'visit_num', 'blog_level']  # 定义info的名字

    csdn_dict = {}
    for index, item in enumerate(lst_name):
        csdn_dict[item] = lst_info[index]
    return csdn_dict


def run():
    """
    执行程序:csdn url→html→提取信息→该作者信息字典返回
    :return:
    """
    url = 'https://blog.csdn.net/KWSY2008'
    html = url_to_html(url)
    csdn_dict = get_blogger_info(html)
    return csdn_dict


if __name__ == '__main__':
    # url = 'https://blog.csdn.net/KWSY2008'
    # html = url_to_html(url)
    # print(get_blogger_info)
    with open('../csdn.txt', encoding='utf-8') as f:
        print(get_blogger_info(f.read()))
