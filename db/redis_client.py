# import redis
# <<<<<<< HEAD
# from conf.redis_config import DICT_CONNECT_REDIS, NAME_QUEUE_REDIS
#
# def store_urllist_to_redis(dict_connect_redis, list_url, name_queue):
#     r = redis.Redis(host=dict_connect_redis["host"],
#                     port=dict_connect_redis["port"],
#                     db=dict_connect_redis["db"])
#     for url in list_url:
#         r.lpush(name_queue, url)
# def get_oneurl_from_redis(dict_connect_redis, name_queue):
#     r = redis.Redis(host=dict_connect_redis["host"],
#                     port=dict_connect_redis["port"],
#                     db=dict_connect_redis["db"])
#     url = r.rpop(name_queue)
#     return url
# def get_allurl_from_redis(dict_connect_redis, name_queue):
#     url = get_oneurl_from_redis(dict_connect_redis, name_queue)
#     while url != None:
#         print(url)
#         url = get_oneurl_from_redis(dict_connect_redis, name_queue)
#
# if __name__ == '__main__':
#     # list_url = ["322424 2","2","3","4"]
#     # store_urllist_to_redis(DICT_CONNECT_REDIS, list_url, NAME_QUEUE_REDIS)
#     get_allurl_from_redis(DICT_CONNECT_REDIS, NAME_QUEUE_REDIS)
# =======

import redis
from conf import redis_conf

r = redis.Redis(**redis_conf.redis_setting)

def test():
    r.set('foo', 'redis')
    print(r.get('foo'))

    push_queue(redis_conf.QueueConfig.csdn_queue, 'test queue')
    print(r.rpop(redis_conf.QueueConfig.csdn_queue))

def push_queue(queue_name, content):
    r.lpush(queue_name, content)

# def push_list_to_queue(queue_name, list_content):
#     for content in list_content:
#         push_queue(queue_name, content)

def pop_queue(queue_name):
    return r.rpop(queue_name)

if __name__ == '__main__':
    test()

