import requests
from urllib.parse import quote
from lxml import etree
def get_zhuanlan_info(url):
    """
    获取一个专栏的关键信息, 比如专栏的名称, 关注人数
    :param url:
    :return:
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': '',#设置为空即可接收到数据。
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'origin':'https://zhuanlan.zhihu.com',
        'referer':'https://zhuanlan.zhihu.com/c_1099248962871169024',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    r=requests.get(url,headers=headers)
    print(r.status_code)
    d={}
    html=r.text
    tree = etree.HTML(html)
    title = tree.xpath("body/div[@id='root']/div/main/div/header/div/h1[@class]")[0]
    num =tree.xpath('body/div[@id="root"]/div/main/div/header/div/span/button')[0]
    d['专栏标题']=title.text
    d['专栏关注人数']=num.text

    return d



if __name__ == '__main__':
    url = 'https://zhuanlan.zhihu.com/c_1099248962871169024'
    print(get_zhuanlan_info(url))