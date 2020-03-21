import time
from datetime import datetime
from db.redis_client import pop_queue
from db.mongo_clinet import insert, get_data_by_url
from conf import mongo_conf


def run_crawler_worker(queue_name, collection_name, function):
    while True:
        url = pop_queue(queue_name)
        if not url:
            time.sleep(3)
            continue

        if not is_need_crawler(url, collection_name):
            continue

        info = function(url)
        if not info:
            time.sleep(3)
            continue

        insert(collection_name, info)


def is_need_crawler(url, collection_name):
    if collection_name == mongo_conf.PY_WEB_SITE:
        return True

    data = get_data_by_url(collection_name, url)

    if data is None:
        return True

    insert_time = data['insert_time']
    now = datetime.now()

    day_diff = (now - insert_time).days
    if day_diff > 7:
        return True

    return False