from functools import wraps
import time


def retry(retry_count=5, sleep_time=1):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            for i in range(retry_count):
                try:
                    res = func(*args, **kwargs)
                    return res
                except:
                    time.sleep(sleep_time)
                    continue
            return None

        return inner

    return wrapper
