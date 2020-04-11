"""
定时执行任务：
1.执行crawler.baidu_crawler.py
2.执行csdn_crawler.py / pywebsite_crawler.py / zhihu_crawler.py（处理对应消息队列至monogo)
3.去重操作(后期再思考）
4.做生产者和消费者平衡处理CONTENT_NUM(后期再思考）
"""
import schedule
import time
import datetime

import crawler.baidu_crawler
from crawler import csdn_crawler, pywebsite_crawler, zhihu_crawler
import threading
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def schedule_job(job_content, set_time, funciton):
    """
    执行任务
    :param job_content: 任务描述
    :param set_time: 任务执行时间，str
    :param funciton: 任务执行的封包函数
    :return:
    """
    logger.info('{}每天{}开始执行'.format(job_content, set_time))
    logger.info('{}-startTime:{}'.format(job_content, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    funciton()
    time.sleep(20)
    logger.info('{}-endTime:{}'.format(job_content, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    logger.info('------------------------------------------------------------------------')


def job1():
    schedule_job("百度抓取任务", "10:00", crawler.baidu_crawler.run)


def job2():
    schedule_job("处理知乎消息队列", "11:00", zhihu_crawler.run)


def job3():
    schedule_job("处理Csdn消息队列", "11:00", csdn_crawler.run)


def job4():
    schedule_job("处理python网站消息队列", "11:00", pywebsite_crawler.run)


def job1_task():
    threading.Thread(target=job1).start()


def job2_task():
    threading.Thread(target=job2).start()


def job3_task():
    threading.Thread(target=job3).start()


def job4_task():
    threading.Thread(target=job4).start()


if __name__ == '__main__':
    schedule.every().day.at('11:25').do(job1_task)
    schedule.every().day.at('11:26').do(job2_task)
    schedule.every().day.at('11:27').do(job3_task)
    schedule.every().day.at('11:28').do(job4_task)
    while True:
        schedule.run_pending()
        time.sleep(60)
        logger.info("Schedule_Job ALIVE - {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
