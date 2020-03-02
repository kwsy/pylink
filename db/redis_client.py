import redis
from conf.redis_config import DICT_CONNECT_REDIS, NAME_QUEUE_REDIS

def store_urllist_to_redis(dict_connect_redis, list_url, name_queue):
    r = redis.Redis(host=dict_connect_redis["host"],
                    port=dict_connect_redis["port"],
                    db=dict_connect_redis["db"])
    for url in list_url:
        r.lpush(name_queue, url)
def get_oneurl_from_redis(dict_connect_redis, name_queue):
    r = redis.Redis(host=dict_connect_redis["host"],
                    port=dict_connect_redis["port"],
                    db=dict_connect_redis["db"])
    url = r.rpop(name_queue)
    return url
def get_allurl_from_redis(dict_connect_redis, name_queue):
    url = get_oneurl_from_redis(dict_connect_redis, name_queue)
    while url != None:
        print(url)
        url = get_oneurl_from_redis(dict_connect_redis, name_queue)

if __name__ == '__main__':
    # list_url = ["322424 2","2","3","4"]
    # store_urllist_to_redis(DICT_CONNECT_REDIS, list_url, NAME_QUEUE_REDIS)
    get_allurl_from_redis(DICT_CONNECT_REDIS, NAME_QUEUE_REDIS)