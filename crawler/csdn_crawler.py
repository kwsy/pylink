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
    res = session.get(url,headers=headers)
    etree_html = etree.HTML(res.text)
    basic1_node = etree_html.xpath('//div[@class="data-info d-flex item-tiling"]/dl')

    info1 = {
        'original content': int(basic1_node[0].attrib['title']),
        'fan': int(basic1_node[1].attrib['title']),
        'like': int(basic1_node[2].attrib['title']),
        'comment': int(basic1_node[3].attrib['title']),
        'visit': int(basic1_node[4].attrib['title'])
    }

    basic2_node = etree_html.xpath('//dl[@class="aside-box-footerClassify"]/dd/a')[0]
    basic3_node = etree_html.xpath('//div[@class="grade-box clearfix"]/dl')[1]
    basic4_node = etree_html.xpath('//div[@class="grade-box clearfix"]/dl[3]/dd')[0]
    basic5_node = etree_html.xpath('//div[@class="grade-box clearfix"]/dl')[3]

    info2 = {
      'grade': basic2_node.attrib['title'].split(',')[0],
      'weekly rank': int(basic3_node.attrib['title']),
      'integral':int(basic4_node.attrib['title']),
      'general rank': int(basic5_node.attrib['title'])
    }

    return dict(info1,**info2)


if __name__ == '__main__':
    url = 'https://blog.csdn.net/KWSY2008'
    print(get_blogger_info(url))