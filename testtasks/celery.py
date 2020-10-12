import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testtasks.settings')

app = Celery('testtasks')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-tasks': {
        'task': 'taskmanager.tasks.check_tasks',
        'schedule': crontab(hour=0, minute=0),
    },
}
