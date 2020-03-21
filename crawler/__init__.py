from db.mongo_client import mongo_client_insert, mongo_client_update, judge_insert_time
from db.redis_client import rpop_queue
import time
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

localtime = time.strftime("%Y-%m-%d", time.localtime(time.time()))


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
            judge_insert_time(content["href"], mongo_name, content, localtime)  # 去重操作

        except Exception as e:
            logger.info("{}消息队列已空，暂无数据处理".format(queue_name), e)
            time.sleep(3)
