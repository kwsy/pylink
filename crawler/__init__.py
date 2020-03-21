from db.redis_client import pop_queue
from db.mongo_client import insert
import time

def run_crawler_worker(queue_name,collection_name,function):
    # url = pop_queue(queue_name)
    # info = function(url)
    # res = insert(collection_name,info)
    # return res

    while True:
        url = pop_queue(queue_name)
        if not url:
            time.sleep(3)
            continue

        info = function(url)
        if not info:
            time.sleep(3)
            continue

        insert(collection_name,info)



