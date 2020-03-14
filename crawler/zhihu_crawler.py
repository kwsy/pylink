from lxml import etree
import requests
import re

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
    res = session.get(url, headers=headers)
    tree = etree.HTML(res.text)
    userlink_node = tree.xpath('//a[@class="UserLink-link"]')[0]
    href = 'https:'+userlink_node.attrib['href'] + '/columns'

    return get_zhuanlan_info2(href)


def get_zhuanlan_info2(url):
    lst = []
    session = requests.session()
    res = session.get(url, headers=headers)
    etree_html= etree.HTML(res.text)

    columns_name_node = etree_html.xpath('//div[@class="ContentItem-head"]')
    for i in columns_name_node:
        name = i.xpath('.//h2/a/div/div')[0]
        # 问题1，为什么print会有2个值，return只有1个值
        name = name.text
        specific_info = i.xpath('.//div[@class="ContentItem-status"]')[0]
        specific_info_text = specific_info.xpath('string(.)')
        specific_info_count = specific_info_text.split(' ')

        info = {
            'name': name,
            'publish': int(specific_info_count[1]),
            'total article': int(specific_info_count[3]),
            'followers': int(''.join(re.findall('\d',specific_info_count[4])))
            # findall 提取字符串里的数字部分，join串联各个数字成为一个整体的数字
        }

        lst.append(info)
        # 问题2：同问题1，为什么print会有2个值，return只有1个值
    return lst


if __name__ == '__main__':
    url = 'https://zhuanlan.zhihu.com/p/109450078'
    print(get_zhuanlan_info(url))
    # 问题3：如何去掉最后打印处来的None




