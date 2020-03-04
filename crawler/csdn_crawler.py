from crawler.pywebsite_crawler import get_html_from_url, get_infolist_from_html_byxpath
def get_blogger_info(url):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    :param url:
    :return:
    """
    html = get_html_from_url(url)
    # string_xpath_people_url = "//dt/a[@data-report-query='t=1']/text()"       # 获取专业专栏作者链接
    string_xpath_people_url = "//d1/text()"       # 获取专业专栏作者链接
    list_people = get_infolist_from_html_byxpath(html, string_xpath_people_url)

    print(list_people)




if __name__ == '__main__':
    url = 'https://blog.csdn.net/KWSY2008'

    # print(get_blogger_info)

    get_blogger_info(url)