import redis
import conf.redis_conf as cf #从conf文件夹下的redis_conf.py文件中引用全局变量
from conf.redis_conf import redis_db #从conf文件夹下的redis_conf.py文件中引用字典
from conf.redis_conf import RedisConfig#从conf文件夹下的redis_conf文件中应引用类

r_global=redis.Redis(host=cf.HOST,port=cf.PORT,password=cf.PASSWORD,db=cf.DB)#引用全局变量

r_dict = redis.Redis(**redis_db)#解包，将字典解包成关键词参数

r_class = redis.Redis(host=RedisConfig.host, port =RedisConfig.port,password=RedisConfig.port,db=RedisConfig.db)

def test_global():
    r_global.set('name','root')#r.set()
    print(r_global.get('name'))#r.get()


def test_dict():
    r_dict.set('name','root')
    print(r_dict.get('name'))


if __name__ == '__main__':
    test_global()
    test_dict()