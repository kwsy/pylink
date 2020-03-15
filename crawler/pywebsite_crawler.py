from lxml import etree
import requests




def judge_py_website(url):
    """
    判断url是一个与python非常相关的网站
    :param url:
    :return:
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    res = requests.get(url,headers=headers)
    res.encoding = 'utf-8'
    tree = etree.HTML(res.text)

    if judge_by_keywords_description(tree):
        return True
    if judge_by_menu(tree):
        return True

    return False


def judge_by_keywords_description(tree):
    if _judge_by_keywords_description(tree,'keywords'):
        return True
    if _judge_by_keywords_description(tree,'description'):
        return True

    return False


def _judge_by_keywords_description(tree,tag):
    """
    利用Keywords，description判断网站相关性
    :param tree:
    :param tag:
    :return:
    """
    node = tree.xpath('//meta[@name="{tag}"]'.format(tag=tag))[0]
    content = node.attrib['content'].lower()

    if content.find('python') != -1 and content.find('教程') != -1:
        return True

    return False



def judge_by_menu(tree):
    """
    利用网站菜单拦判断网站相关性
    :param html:
    :return:
    """
    menu_node = tree.xpath('//ul[@id="main-menu"]/li/a')
    for menu_content in menu_node:
        content = menu_content.text.lower()
        if content.find('python') != -1 and content.find('教程') != -1:
            return True
    return False



if __name__ == '__main__':
    url = 'http://www.kidscode.cn/python'
    print(judge_py_website(url))

    url = 'https://www.itcodemonkey.com/'
    print(judge_py_website(url))