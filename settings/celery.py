import os
from celery import Celery
# from kombu import Queue

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

app = Celery('settings')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.task_queues = (
#     Queue('celery', routing_key='worker_1'),
# )
# app.conf.task_default_queue = 'celery'