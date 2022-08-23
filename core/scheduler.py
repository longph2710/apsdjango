import logging

from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import register_events, register_job, DjangoJobStore

from django.conf import settings

from core.models import *

# Config jobstore optionnal
jobstore = {
    'djangojobstore' : DjangoJobStore()
}
# Create scheduler to run in a thread inside the application process
scheduler = BackgroundScheduler(settings.SCHEDULER_CONFIG, jobstore='djangojobstore')

def start():
    if not settings.DEBUG:
      	# Hook into the apscheduler logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # Adding job to extend lock timeout

    # Add the scheduled jobs to the Django admin interface
    register_events(scheduler)

    scheduler.start()