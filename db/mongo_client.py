"""
建立mongo连接
@time ： 2020年3月12日23点31分
@author : hjf
"""
import pymongo

mongo_client_hjf = pymongo.MongoClient(host=None,
                                       port=None,
                                       document_class=dict,
                                       tz_aware=None,
                                       connect=None,
                                       type_registry=None)
gjgh