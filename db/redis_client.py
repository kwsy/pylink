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


def pop_queue(queue_name):
    res = r.rpop(queue_name)
    return res.decode()



if __name__ == '__main__':
    test()