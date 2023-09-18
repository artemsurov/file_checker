import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

app = Celery('conf')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'validate-files-task-ten-seconds': {
        'task': 'validate_files_task',
        'schedule': 10.0,
        'args': []
        }
    }
