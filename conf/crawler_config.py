"""
请在脚本里配置爬虫参数
"""

# 数据保存文件配置
FLAG_SAVE_HTMLFILE = 0                   # 是否存储html数据至指定文件夹
PATH_HTMLFILE = "../data/htmlfile"       # html数据存储路径

FLAG_SAVE_URLFILE = 0                    # 是否存储url数据至指定文件夹
PATH_URLFILE = "../data/urlfile"         # url数据存储路径

# 搜索引擎配置
URL_BAIDU = 'https://www.baidu.com/s'    # 搜索引擎url

# 爬虫参数配置

TOTALNUM_SEARCH_PAGE = 50               # 单个关键词搜索引擎爬取页数

TIMES_REQUESTS_MAX = 5                   # request请求异常重复请求最大次数
TIME_REQUEST_SLEEP = 5                   # request请求间隔时间

