from crawler.pywebsite_crawler import get_html_from_url, get_keyinfolist_from_html

from urllib import parse

page_url = 'http://fcg.gxepb.gov.cn/ztzl/hjwfbgt/'
new_url = '../../hjzf/xzcf/201811/t20181102_46347.html'

new_full_url = parse.urljoin(page_url, new_url)


# def get_zhuanlan_info(url):
#     """
#     获取一个专栏的关键信息, 比如专栏的名称, 关注人数
#     :param url:
#     :return:
#     """
#     pass


# if __name__ == '__main__':
#     url = 'https://zhuanlan.zhihu.com/c_1099248962871169024'
#     print(get_zhuanlan_info(url))



def get_peopleurl_from_zhuanlanurl(url):

    html = get_html_from_url(url)

    # string_xpath_people = "//a[@class='UserLink-link']"                # 获取专栏作者名
    # list_people = get_keyinfolist_from_html(html, string_xpath_people)
    # people = list_people[0].text

    string_xpath_people_url = "//a[@class='UserLink-link']/@href"       # 获取专业专栏作者链接
    list_people = get_keyinfolist_from_html(html, string_xpath_people_url)
    people_url = list_people[0]

    base_url = "https://www.zhihu.com/people/"
    last_url = parse.urljoin(base_url, people_url)

    print("last_url:{}".format(last_url))
    return last_url

def get_destinationurl_from_peopleurl(url):

    html = get_html_from_url(url)

    string_xpath_people_url = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"       # 获取专业专栏作者链接
    list_destinationurl = get_keyinfolist_from_html(html, string_xpath_people_url)
    destination_url = list_destinationurl[0]

    base_url = "https://www.zhihu.com/people/"
    last_url = parse.urljoin(base_url, destination_url)

    print(last_url)
    return last_url

def get_peopleinfo_from_destinationurl(url):
    html = get_html_from_url(url)

    #获取people ID信息
    string_xpath_people_id = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"  # 获取专业专栏作者链接
    #获取专栏信息（数量、专栏名称）
    string_xpath_people_zhuanlannum = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"  # 获取专业专栏作者链接
    string_xpath_people_zhuanlanname = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"  # 获取专业专栏作者链接
    #获取个人成就信息(赞同、喜欢、收藏)
    string_xpath_people_achieve_agree = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"  # 获取专业专栏作者链接
    string_xpath_people_achieve_love = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"  # 获取专业专栏作者链接
    string_xpath_people_achieve_store = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"  # 获取专业专栏作者链接
    #获取关注信息（关注别人、被别人关注）
    string_xpath_people_concern_others = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"  # 获取专业专栏作者链接
    string_xpath_people_concern_byothers = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"  # 获取专业专栏作者链接




def get_zhuanlan_info(url):
    """
    获取一个专栏的关键信息, 比如专栏的名称, 关注人数
    :param url:
    :return:
    """

    # 从专栏获取专栏people
    # 从专栏people获取people所有专栏
    pass
url = 'https://zhuanlan.zhihu.com/c_1099248962871169024'
people_url = get_peopleurl_from_zhuanlanurl(url)
# get_destinationurl_from_peopleurl("http://www.zhihu.com/people/coolpython")