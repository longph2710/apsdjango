from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, register_job, DjangoJobStore, DjangoMemoryJobStore

from django.conf import settings

from core.models import *

import redis_lock
import redis

# config lock 
conn = redis.Redis()
lock_scheduler = redis_lock.Lock(conn, name='django-scheduler-locker-01', expire=50)

# config scheduler
mem_scheduler = BackgroundScheduler()
django_scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG)

# extend expiration time for all lock
def extend_expiration_time(expire=45):
    if mem_scheduler.running:
        mem_scheduler.shutdown()
    lock_scheduler.extend(expire=expire)
    print('[%s] extend 1' % datetime.now())

def start_scheduler():
    django_scheduler.start()
    print('scheduler started!')

def check_lock_scheduler():
    if lock_scheduler.acquire(timeout=10):
        print('got lock scheduler!')
        mem_scheduler.pause()

        django_scheduler.add_job(
            id='job-extend-expiration-time-01',
            func=extend_expiration_time,
            trigger='interval',
            seconds=30,
            replace_existing=True
        )
        django_scheduler.start()
        print('scheduler started!')
    else:
        print('someone has lock scheduler!')

def start():
    if not mem_scheduler.running and settings.SCHEDULER_AUTOSTART:
        print('start memory scheduler!')
        mem_scheduler.add_job(
            id='checking-lock-scheduler', 
            func=check_lock_scheduler,
            trigger='interval',
            seconds=10,
            replace_existing=True
        )

        mem_scheduler.start()