'''

 消息队列的参数配置：全局变量
'''
HOST='101.201.225.172'
PORT=6379
PASSWORD='198671724zds!'
DB=1

'''

 消息队列的参数配置：字典
'''

redis_db={'host':'101.201.225.172',
          'port':6379,
          'password':'198671724zds!',
          'db':1}

'''
消息队列的参数配置:类
'''
class RedisConfig:
    host = "127."
    port = 6379
    password = '198671724zds!'
    db=1

class QueueConfig:
    csdn_queue='csdn_blog_queue' #创建三个消息队列
    zhihu_queue = 'zhihu_zhuanlan_queue'
    py_website ='py_website_queue'

