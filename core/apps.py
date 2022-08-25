from django.apps import AppConfig

from django.conf import settings

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from . import scheduler
        if settings.SCHEDULER_AUTOSTART:
        	scheduler.start()