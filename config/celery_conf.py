import os
from celery import Celery
from datetime import timedelta
from kombu import Queue, Exchange
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

celery_app = Celery('config', )
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks(packages=['rating.tasks'])

celery_app.conf.result_expires = timedelta(days=1)

celery_app.conf.beat_schedule = {
    'update-ratings-every-hour': {
        'task': 'rating.tasks.update_ratings',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}