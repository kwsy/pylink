from crawler.pywebsite_crawler import get_html_from_url
from conf import redis_conf
from conf import mongo_conf
from db import redis_client
from db import mongo_client
import requests
from lxml import etree
import time

def get_blogger_info(url):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    :param url:
    :return:
    """
    blogger_info = {}
    session = requests.session()
    html = get_html_from_url(session, url)
    tree = etree.HTML(html)

    blogger_info['博主'] = tree.xpath("//div[@class='profile-intro d-flex']/div/div/span/a/@title")[0]

    blogger_info['原创'] = tree.xpath("//div[@id='asideProfile']//dl[@class='text-center'][1]/@title")[0]
    blogger_info['粉丝'] = tree.xpath("//div[@id='asideProfile']//dl[@class='text-center'][2]//span/text()")[0]
    blogger_info['获赞'] = tree.xpath("//div[@id='asideProfile']//dl[@class='text-center'][3]//span/text()")[0]
    blogger_info['评论'] = tree.xpath("//div[@id='asideProfile']//dl[@class='text-center'][4]//span/text()")[0]
    blogger_info['访问'] = tree.xpath("//div[@id='asideProfile']//dl[@class='text-center'][5]//span/text()")[0]

    blogger_info['周排名'] = tree.xpath("//div[@class='grade-box clearfix']//dl[@title][1]/@title")[0]
    blogger_info['总排名'] = tree.xpath("//div[@class='grade-box clearfix']//dl[@title][2]/@title")[0]

    blogger_info['url'] = url

    # print(blogger_info)
    return blogger_info

def csdn_run():
    while True:
        url = redis_client.pop_queue(redis_conf.QueueConfig.csdn_queue)
        print(url)
        if  url == None:
            time.sleep(10)
            continue
        blogger_info = get_blogger_info(url)
        mongo_client.collection_insert_one_csdn(blogger_info)
        print(blogger_info)
def csdn_test():
    url = 'https://blog.csdn.net/KWSY2008'
    blogger_info = get_blogger_info(url)
    mongo_client.collection_insert_one_csdn(blogger_info)
    for x in mongo_client.collection_csdn.find():
        print(x)

if __name__ == '__main__':
    # csdn_test()
    csdn_run()