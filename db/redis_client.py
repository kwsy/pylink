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


def rpop_queue(queue_name):
    """
    读取消息队列内容,由byte转化为str
    :param queue_name:
    :return:
    """
    url_byte = connect_redis.rpop(queue_name)
    if url_byte:
        url = url_byte.decode(encoding='utf-8')
        return url


def test():
    """
    测试redis是否连接成功
    :return:
    """
    connect_redis.set('far', 'soo')
    print(connect_redis.get('far'))  # 返回b'soo',b是指bytes字节串类型,存储数据量小
    print(type(connect_redis.get('far')))
    lpush_queue(redis_conf.QueueConfig.test, 'test queue')
    lpush_queue(redis_conf.QueueConfig.test, 'test queue2')
    lpush_queue(redis_conf.QueueConfig.test, 'test queue3')
    # print(connect_redis.rpop(redis_conf.QueueConfig.csdn_queue))    # 按输入顺序，每次只取一条，先入先出
    for i in range(3):
        print(rpop_queue(redis_conf.QueueConfig.test))
    # 测试完毕 清空csdn_queue的内容
    connect_redis.flushdb(redis_conf.QueueConfig.test)    # 测试完毕 清空csdn_queue的内容


if __name__ == "__main__":
    test()
