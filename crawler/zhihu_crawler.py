import requests
import time
from lxml import etree
from db import redis_client
from conf.redis_conf import QueueConfig
from crawler import run_crawler_worker
from conf.mongo_conf import ZHIHU_COLLECTION

headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }


def get_zhuanlan_info(url):
    """
    获取一个专栏的关键信息, 比如专栏的名称, 关注人数
    :param url:
    :return:
    """
    session = requests.session()
    href = get_zhuanlan_columns_url(session, url)
    time.sleep(2)

    data = get_zhuanlan_info_columns(session, href)
    info = {'blog_url': href, 'zhuanlan': data}
    return info

def get_zhuanlan_columns_url(session, url):
    res = session.get(url, headers=headers)
    tree = etree.HTML(res.text)
    user_node = tree.xpath('//a[@class="UserLink-link"]')[0]
    href = user_node.attrib['href']
    if not href.startswith('https'):
        href = "https:" + href + '/columns'

    return href


def get_zhuanlan_info_columns(session, url):
    zhuanlan_lst = []
    res = session.get(url, headers=headers)
    tree = etree.HTML(res.text)
    lst = tree.xpath('//div[@class="List-item"]')

    for item in lst:
        title_node = item.xpath('.//h2[@class="ContentItem-title"]/a/div/div')[0]
        title = title_node.text

        publish_node = item.xpath('.//div[@class="ContentItem-status"]/a')[0]
        publish_text = publish_node.xpath('string(.)')
        publish_count = int(publish_text.split()[1])

        follow_node = item.xpath('.//div[@class="ContentItem-status"]/span[2]')[0]
        follow_count = int(follow_node.text.split()[0])

        info = {
            'name': title,
            'publish_count': publish_count,
            'follow_count': follow_count
        }
        zhuanlan_lst.append(info)

    return zhuanlan_lst

def run():
    run_crawler_worker(QueueConfig.zhihu_queue, ZHIHU_COLLECTION, get_zhuanlan_info)

def test():
    redis_client.push_queue(QueueConfig.zhihu_queue, 'https://zhuanlan.zhihu.com/p/109450078')
    run_crawler_worker(QueueConfig.zhihu_queue, ZHIHU_COLLECTION, get_zhuanlan_info)


if __name__ == '__main__':
    # url = 'https://zhuanlan.zhihu.com/p/109450078'
    # print(get_zhuanlan_info(url))
    test()