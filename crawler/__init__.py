import time
from db.redis_client import pop_queue
from db.mongo_clinet import insert


def run_crawler_worker(queue_name, collection_name, function):
    while True:
        url = pop_queue(queue_name)
        if not url:
            time.sleep(3)
            continue

        info = function(url)
        if not info:
            time.sleep(3)
            continue

        insert(collection_name, info)
