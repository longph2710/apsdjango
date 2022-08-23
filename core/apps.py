from django.apps import AppConfig

from django.conf import settings

from redis import Redis
import time
import redis_lock

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        
        conn = Redis()
        lock = redis_lock.RedisLock(conn, "lock-django-03")
        while True:
            if lock.acquire():
                print('got lock')
                break
            else: 
                print('someone has lock!')
                time.sleep(10)
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
        	scheduler.start()