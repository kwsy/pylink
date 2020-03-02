import requests
from lxml import etree
from common.url_utils import url_to_html

#html = url_to_html(url)

def get_blogger_info(html):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    :param url:csdn.net为主信息
    :return:
    """

    tree = etree.HTML(html)
    rank = tree.xpath('//div[@class="grade-box clearfix"]/dl[@title]/@title')
    rank_name = tree.xpath('//div[@class="grade-box clearfix"]/dl[@title]/dt/text()')
    information_num = tree.xpath('//div[@class = "data-info d-flex item-tiling"]/dl[@class = "text-center"]/@title')
    information_name = tree.xpath('//div[@class = "data-info d-flex item-tiling"]/dl[@class = "text-center"]/dt/text()')

    match_dict = information_dict(information_name, information_num)
    match_dict.update(information_dict(rank_name,rank))
    print(match_dict)
    return match_dict




def information_dict(name, num):
    '''
    两个列表形成字典
    :param name:
    :param num:
    :return:
    '''
    result = {}
    for i,j in enumerate(name):
        result[j] = num[i]

    return result


if __name__ == '__main__':
    url = 'https://blog.csdn.net/KWSY2008'
    #print(get_blogger_info)
    with open('../csdn.txt', encoding='utf-8') as f:
        print(get_blogger_info(f.read()))