"""
创建 redis连接对象
抓取连接发送q498339146_url_queue
"""
import redis
from conf import redis_conf

connect_redis = redis.Redis(**redis_conf.redis_conf_hjf)


def lpush_queue(queue_name, content):
    """
    将content存储到对应队列名当中
    :param queue_name:队列名
    :param content:内容值
    :return:
    """
    connect_redis.lpush(queue_name, content)

def test():
    """
    测试redis是否连接成功
    :return:
    """
    connect_redis.set('far', 'soo')
    print(connect_redis.get('far')) # 返回b'soo',b是指bytes字节串类型,存储数据量小
    print(type(connect_redis.get('far')))
    lpush_queue(redis_conf.QueueConfig.csdn_queue, 'test queue')
    print(connect_redis.rpop(redis_conf.QueueConfig.csdn_queue))



if __name__ == "__main__":
    test()
