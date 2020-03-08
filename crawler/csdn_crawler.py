from lxml import etree
import requests


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, compress',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'blog.csdn.net',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}


def get_blogger_info(url):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    :param url:
    :return:
    """
    session = requests.session()
    res = requests.get(url,headers=headers)
    etree_html = etree.HTML(res.text)
    basic1_node = etree_html.xpath('//div[@id="asideProfile"/div[@class="data-info d-flex item-tiling"/dl/@title]')

    info1 = {
        'original content': int(basic1_node[0]),
        'fan': int(basic1_node[1]),
        'like': int(basic1_node[2]),
        'comment': int(basic1_node[3]),
        'visit': int(basic1_node[4])
    }

    basic2_node = etree_html.xpath('//div[@id="asideProfile"/div[@class="data-info d-flex item-tiling"/dl/@title]')


    # csdn_info_dict = {}
    # etree_html = etree.HTML(url)
    # res = etree_html.xpath('')




if __name__ == '__main__':
    url = 'https://blog.csdn.net/KWSY2008'
    print(get_blogger_info)