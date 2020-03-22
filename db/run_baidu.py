from apscheduler.schedulers.blocking import BlockingScheduler
from crawler.baidu_crawler import run

scheduler = BlockingScheduler()
scheduler.add_job(run, 'cron', hour=10)   # 每天10点执行百度爬虫
scheduler.start()