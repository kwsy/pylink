from crawler.pywebsite_crawler import get_html_from_url, get_infolist_from_html_byxpath
from conf import redis_conf
from db import redis_client
def get_blogger_info(url):
    """
    获取csdn博客主的信息,比如博客等级, 总排名, 其他任何你想抓取的信息你有能力,都可以抓取
    :param url:
    :return:
    """
    author = {}
    i = 0
    html = get_html_from_url(url)

    string_xpath_people_id = "//span[@class='name csdn-tracking-statistics tracking-click ']/a/text()"  # 获取专业专栏作者链接
    string_xpath_people_keyword1 = "//div[@class='data-info d-flex item-tiling']//dt/a/text()"          # 获取关键字
    string_xpath_people_keyword2 = "//div[@class='data-info d-flex item-tiling']//dt/text()"            # 获取关键字
    string_xpath_people_keynum = "//div[@class='data-info d-flex item-tiling']//span/text()"            # 获取关键值
    string_xpath_people_range_value = "//div[@class='grade-box clearfix']/dl[@title]/dt/text()"         # 获取排名名称
    string_xpath_people_range = "//div[@class='grade-box clearfix']/dl[@title]/dd/a/text()"             # 获取排名值

    string_xpath_people_id = get_infolist_from_html_byxpath(html, string_xpath_people_id)
    string_xpath_people_keyword1 = get_infolist_from_html_byxpath(html, string_xpath_people_keyword1)
    string_xpath_people_keyword2 = get_infolist_from_html_byxpath(html, string_xpath_people_keyword2)
    string_xpath_people_keynum = get_infolist_from_html_byxpath(html, string_xpath_people_keynum)

    string_xpath_people_range = get_infolist_from_html_byxpath(html, string_xpath_people_range)
    string_xpath_people_range_value = get_infolist_from_html_byxpath(html, string_xpath_people_range_value)

    string_xpath_people_keyword = string_xpath_people_keyword1 + string_xpath_people_keyword2
    # print(string_xpath_people_keyword)

    author['id'] = string_xpath_people_id
    for keyword in string_xpath_people_keyword:

        author[keyword] = string_xpath_people_keynum[i]
        i += 1
    i = 0
    for range_value in string_xpath_people_range_value:
        author[range_value] = string_xpath_people_range[i]
        i += 1
    author['url'] = url
    print(author)

def csdn_run():
    while True:
        url = redis_client.pop_queue(redis_conf.QueueConfig.csdn_queue)
        print(url)
        if  url == None:
            break
        dict_author = get_blogger_info(url)
        print(dict_author)

if __name__ == '__main__':
    url = 'https://blog.csdn.net/KWSY2008'
    get_blogger_info(url)
    # csdn_run()