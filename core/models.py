from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

import requests

# Create your models here.

class BackupHistory(models.Model):
    database_id = models.CharField(max_length=20)
    backup_id = models.CharField(max_length=20, null=True)
    performer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_finish = models.DateTimeField()

class JobExe():

    def job_test_1():
        print('[{}] job test 1'.format(datetime.now()))

    def job_test_2():
        print('[{}] job test 2'.format(datetime.now()))
        
    def job_backup_01(id, hours=None, minutes=None, seconds=None):
        print('[%s] backup database: %s' % (datetime.now(), id))

    def call_backup_api(database_id):
        url = 'http://127.0.0.1:8010/app01/backup/?database_id=%s' % database_id
        response = requests.get(url=url)
        print(response)