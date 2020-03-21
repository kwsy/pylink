from apscheduler.schedulers.blocking import BlockingScheduler
from crawler.baidu_crawler import run

sched = BlockingScheduler()
sched.add_job(run, 'cron', hour=10)     # 每天10点执行百度爬虫
sched.start()

