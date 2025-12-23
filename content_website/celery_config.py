import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "content_website.settings")
app = Celery("content_website")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
        
    'task-1': {'task': 'queries.tasks.delete_patients_week_old', 'schedule': crontab(minute='*/1')},
    'task-2': {'task': 'queries.tasks.send_info_to_discord', 'schedule': crontab(minute='*/1')},

}