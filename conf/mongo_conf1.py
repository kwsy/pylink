"""
配置mongo数据库
不能加入仓库，防止密码外泄
"""

mongo_conf_hjf = {'host': '101.201.225.172', 'port': 27019}
db = 'hjf_crawler_db'

class MongoCollection:
    csdn_mongo = 'csdn_hjf'
    pywebsite_mongo = 'pywebsite_hjf'
    zhihu_mongo = 'zhihu_hjf'