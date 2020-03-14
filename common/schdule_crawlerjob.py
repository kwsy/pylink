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
import os
import requests
import crawler.baidu_crawler
from crawler import csdn_crawler, pywebsite_crawler, zhihu_crawler

CONTENT_NUM = crawler.baidu_crawler.CONTENT_NUM


def job1():
    print('Job1:每天6:30执行一次')
    print('Job1-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    crawler.baidu_crawler.run()
    time.sleep(20)
    print('Job1-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')

def job2():
    print('Job2:每天7:30执行一次')
    print('Job2-startTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    csdn_crawler.run()
    time.sleep(5)
    pywebsite_crawler.run()
    time.sleep(5)
    zhihu_crawler.run()
    time.sleep(5)
    time.sleep(20)
    print('Job2-endTime:%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    print('------------------------------------------------------------------------')


if __name__ == '__main__':
    schedule.every().day.at('17:54').do(job1)
    schedule.every().day.at('18:20').do(job1)
    print(CONTENT_NUM)
    while True:
        schedule.run_pending()
        time.sleep(60)
        print("wait", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))