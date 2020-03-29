import requests
from urllib.parse import quote
from lxml import etree
def get_blogger_info(url):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    :param url:
    :return:
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': '',  # 设置为空即可接收到数据。
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'referer': quote('https://zhuanlan.zhihu.com/c_1099248962871169024'),
        #  'Host': 'https://www.zhihu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}

    r=requests.get(url=url,headers=headers)
    print(r.status_code)
    d={}
    html = r.text
    tree = etree.HTML(html)
    title = tree.xpath('/html/body/header/div/div[1]/h1/a')[0]
    author=tree.xpath('//*[@id="uid"]')[0]
    总排名 =tree.xpath('//*[@id="asideProfile"]/div[3]/dl[4]/dt')[0]
    ranking=tree.xpath('//*[@id="asideProfile"]/div[3]/dl[4]')[0]
    等级 =tree.xpath('//*[@id="asideProfile"]/div[3]/dl[1]/dt')[0]
    blog_level=tree.xpath('//*[@id="asideProfile"]/div[3]/dl[1]/dd/a/svg/use')[0]
    原创=tree.xpath('//*[@id="asideProfile"]/div[2]/dl[1]/dt/a')[0]
    yuanchuang_num=tree.xpath('//*[@id="asideProfile"]/div[2]/dl[1]/dd/a/span')[0]

    d['博客标题']=title.text
    d['作者']=author.attrib['title']
    d[总排名.text]=ranking.attrib['title']
    d[等级.text]=blog_level.attrib['xlink:href']
    d[原创.text]=yuanchuang_num.text

    return d

if __name__ == '__main__':
    url = 'https://blog.csdn.net/KWSY2008'
    print(get_blogger_info(url))