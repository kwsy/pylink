import redis
from conf import redis_conf


# 方法1 普通连接
# r = redis.Redis(host=redis_conf.host,password=redis_conf.password,port=redis_conf.port,db=redis_conf.db)


# 方法2 利用字典
# r = redis.Redis(host=redis_conf.RedisConfig.host,password=redis_conf.RedisConfig.password,port=redis_conf.RedisConfig.port,db=redis_conf.RedisConfig.db)


# 方法3 利用类
r = redis.Redis(**redis_conf.redis_setting)


# 方法4
# 连接池连接（可以减少频繁的连接、断开数据库的开销）
# try:
#     r = redis.Redis(host='101.201.225.172', password='198671724zds!', port=6379, db=1)
#     print("connected success.")
# except:
#     print("could not connect to redis.")


def test():
    r.set('foo','redis')
    print(r.get('foo'))

    push_queue(redis_conf.QueueConfig.csdn_queue, 'test queue')
    print(r.rpop(redis_conf.QueueConfig.csdn_queue))


def push_queue(queue_name, content):
    r.lpush(queue_name, content)

def pop_queue(queue_name):
    url_byte = r.rpop(queue_name)
    if not url_byte:
        return None
    url = url_byte.decode(encoding='utf-8')
    return url


if __name__ == '__main__':
    test()