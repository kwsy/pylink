import redis
from conf.redis_conf import RedisConfig, QueueConfig
sr = redis.StrictRedis(host=RedisConfig.host, port=RedisConfig.port, db=RedisConfig.db)


def ftest():
    sr.set('foo', 'redis')
    print(sr.get('foo'))
    push_queue(QueueConfig.csdn_queue, 'csdn')
    print(sr.rpop(QueueConfig.csdn_queue))


def push_queue(queue_name, content):
    sr.lpush(queue_name, content)


if __name__ == '__main__':
    ftest()