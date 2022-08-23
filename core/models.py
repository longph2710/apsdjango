from asyncio.windows_events import NULL
from datetime import datetime
from django.db import models

# Create your models here.

class JobExe():

    def job_test_1():
        print('[{}] job test 1'.format(datetime.now()))

    def job_test_2():
        print('[{}] job test 2'.format(datetime.now()))
        
    def job_backup_01(id, hours=None, minutes=None, seconds=None):
        print('[%s] backup database: %s' % (datetime.now(), id))