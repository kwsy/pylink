from db.mongo_client import mongo_client_insert, mongo_client_update, mongo_find_collect
from db.redis_client import rpop_queue
from conf.mongo_conf1 import MongoCollection
import time
from datetime import datetime
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_need_crawler(url, mongo_name):
    if mongo_name == MongoCollection.pywebsite_mongo:
        return True
    data = mongo_find_collect(mongo_name, url)
    if data is None:
        return True
    insert_time = data['insert']
    now = datetime.now()
    if d


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
            if not is_need_crawler(url, mongo_name):
                continue
            content = function(url)
            print(content)
            if not content:
                time.sleep(3)
                continue
            mongo_client_update(content["href"], mongo_name, content)  # 去重操作

        except Exception as e:
            logger.info("{}消息队列".format(queue_name), e)
            time.sleep(3)
