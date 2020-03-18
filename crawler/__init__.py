from db.mongo_client import mongo_client_insert
from db.redis_client import rpop_queue
import time


def run_crawler_worker(queue_name, mongo_name, function):
    """
    执行程序:url→提取信息→存储至monogo
    :return:
    """
    while True:
        try:
            url = rpop_queue(queue_name)  # 增加去重操作
            if not url:
                time.sleep(3)
                continue
            print(url)
            content = function(url)
            print(content)
            if not content:
                time.sleep(3)
                continue
            mongo_client_insert(mongo_name, content)  # 去重操作

        except Exception as e:
            print("{}消息队列已空，暂无数据处理".format(queue_name), e)
            time.sleep(3)
