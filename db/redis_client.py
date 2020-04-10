import redis
import conf.redis_conf as cf #从conf文件夹下的redis_conf.py文件中引用全局变量
from conf.redis_conf import redis_db #从conf文件夹下的redis_conf.py文件中引用字典
from conf.redis_conf import * #从conf文件夹下的redis_conf文件中应引用类

r_global=redis.Redis(host=cf.HOST,port=cf.PORT,password=cf.PASSWORD,db=cf.DB)#引用全局变量

r_dict = redis.Redis(**redis_db)#解包，将字典解包成关键词参数 #建立连接与redis数据库

r_class = redis.Redis(host=RedisConfig.host, port =RedisConfig.port,password=RedisConfig.port,db=RedisConfig.db)

def test_global():
    r_global.set('name','root')#r.set()
    print(r_global.get('name'))#r.get()


def test_dict():
    r_dict.set('name','root')
    print(r_dict.get('name'))
    push_queue(QueueConfig.csdn_queue,'test queue')#创建一个消息队列写入数据test queue
    print(r_dict.rpop(QueueConfig.csdn_queue))#写入后再读取出来


def push_queue(queue_name,content):#专门写一个函数用于把数据push到消息队列里面
    r_dict.lpush(queue_name,content)



if __name__ == '__main__':
    test_global()
    test_dict()