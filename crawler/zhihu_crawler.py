from crawler.pywebsite_crawler import get_html_from_url, get_infolist_from_html_byxpath
from urllib import parse
from conf import redis_conf
from db import redis_client

def get_peopleurl_from_zhuanlanurl(url):
    html = get_html_from_url(url)

    string_xpath_people_url = "//a[@class='UserLink-link']/@href"       # 获取专业专栏作者链接
    list_people = get_infolist_from_html_byxpath(html, string_xpath_people_url)
    people_url = list_people[0]

    base_url = "https://www.zhihu.com/people/"
    last_url = parse.urljoin(base_url, people_url)

    return last_url

def get_destinationurl_from_peopleurl(url):
    html = get_html_from_url(url)

    string_xpath_people_url = "//li[@aria-controls='Profile-columns']/a[@class='Tabs-link']/@href"       # 获取专业专栏作者链接
    list_destinationurl = get_infolist_from_html_byxpath(html, string_xpath_people_url)
    print("list_destinationurl")
    print(list_destinationurl)
    destination_url = list_destinationurl[0]

    base_url = "https://www.zhihu.com/people/"
    last_url = parse.urljoin(base_url, destination_url)
    print(last_url)
    return last_url

def get_peopleinfo_from_destinationurl(url):
    author = {}
    list_zhuanlan = []
    dict_temp_zhuanlan = {}
    html = get_html_from_url(url)

    # 获取people ID信息
    string_xpath_people_id = "//span[@class='ProfileHeader-name']/text()"                           # 获取专栏作者ID
    # 获取专栏信息（数量、专栏名称）
    string_xpath_people_zhuanlan_num = "//li[@aria-controls='Profile-columns']/a/span/text()"       # 获取专栏数量
    string_xpath_people_zhuanlan_name =  "//div[@class='ListShortcut']//div/text()"                    # 获取专栏名称及描述（所有列表）
    string_xpath_people_zhuanlan_information = "//div[@class='ListShortcut']//span[@class = 'ContentItem-statusItem']/text()"      # 获取专栏文章及关注信息（所有列表）

    zhuanlan_id = get_infolist_from_html_byxpath(html, string_xpath_people_id)
    zhuanlan_num = get_infolist_from_html_byxpath(html, string_xpath_people_zhuanlan_num)
    list_zhuanlan_name = get_infolist_from_html_byxpath(html, string_xpath_people_zhuanlan_name)
    list_zhuanlan_information = get_infolist_from_html_byxpath(html, string_xpath_people_zhuanlan_information)

    author['id'] = zhuanlan_id[0]
    author['zhuanlan_num'] = zhuanlan_num[0]
    if len(list_zhuanlan_name) != len(list_zhuanlan_information):  # 去除部分页面布局与常规异常，后续考虑完善
        print("html结构与其他异常")
        return author

    for i in range(int(author['zhuanlan_num'])):
        dict_temp_zhuanlan['name'] = list_zhuanlan_name[2*i]
        dict_temp_zhuanlan['describe'] = list_zhuanlan_name[2*i+1]
        dict_temp_zhuanlan['num_article'] = list_zhuanlan_information[2*i]
        dict_temp_zhuanlan['num_followers'] = list_zhuanlan_information[2*i+1]

        list_zhuanlan.append(dict_temp_zhuanlan)

    author['zhuanlan_info'] = list_zhuanlan
    return author

def get_zhuanlan_info(url):
    """
    获取一个专栏的关键信息, 比如专栏的名称, 关注人数
    :param url:
    :return:
    """
    people_url = get_peopleurl_from_zhuanlanurl(url)
    url_destination = get_destinationurl_from_peopleurl(people_url)
    dict_author = get_peopleinfo_from_destinationurl(url_destination)

    return dict_author

#　模拟测试用url
list_url_queue=["https://zhuanlan.zhihu.com/p/52580843",
                "https://zhuanlan.zhihu.com/p/36581953",
                'https://zhuanlan.zhihu.com/c_1099248962871169024'
                ]

def push_list_to_queue(queue_name, list_content):
    for content in list_content:
        redis_client.push_queue(queue_name, content)

def redis_test():
    push_list_to_queue(redis_conf.QueueConfig.zhihu_queue, list_url_queue)
    while True:
        url = redis_client.pop_queue(redis_conf.QueueConfig.zhihu_queue)
        print(url)
        if  url == None:
            break
        dict_author = get_zhuanlan_info(url)
        print(dict_author)

def zhihu_run():
    while True:
        url = redis_client.pop_queue(redis_conf.QueueConfig.zhihu_queue)
        print(url)
        if  url == None:
            break
        dict_author = get_zhuanlan_info(url)
        print(dict_author)

if __name__ == '__main__':
    # url = 'https://zhuanlan.zhihu.com/c_1099248962871169024'
    # dict_author = get_zhuanlan_info(url)
    # print(dict_author)

    redis_test()
    # zhihu_run()


