"""
请在脚本里配置爬虫参数
"""

# 数据保存文件配置
FLAG_SAVE_HTMLFILE = 1                   # 是否存储html数据至指定文件夹
PATH_HTMLFILE = "../data/htmlfile"       # html数据存储路径

FLAG_SAVE_URLFILE = 1                    # 是否存储url数据至指定文件夹
PATH_URLFILE = "../data/urlfile"         # url数据存储路径

# 搜索引擎配置
URL_BAIDU = 'https://www.baidu.com/s'    # 搜索引擎url

# 爬虫参数配置
TIMES_ERR_304_MAX = 3                    # 304异常重复请求次数
TOTALNUM_SEARCH_PAGE = 10                # 单个关键词搜索引擎爬取页数

TIME_PAGE_SLEEP = 1                      # 爬取每页间隔时间
TIME_GETREALURL_SLEEP = 0.001            # 获取真实url间隔时间

# 这些都是程序里临时用到的,不是配置项,不要写在这里
LIST_URL_ONEKEYWORD = []                 # 单个关键词搜索结果url列表
LIST_URL_ALLKEYWORD = []                 # 所有关键词搜索结果url列表


