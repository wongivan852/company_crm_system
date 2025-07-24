# celery.py
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_project.settings')

app = Celery('crm_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Periodic tasks
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-course-reminders': {
        'task': 'crm.tasks.send_course_reminders',
        'schedule': crontab(hour=9, minute=0),  # Daily at 9 AM
    },
    'send-weekly-newsletter': {
        'task': 'crm.tasks.send_weekly_newsletter',
        'schedule': crontab(hour=10, minute=0, day_of_week=1),  # Monday at 10 AM
    },
    'cleanup-old-logs': {
        'task': 'crm.tasks.cleanup_old_communication_logs',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),  # Sunday at 2 AM
    },
}

app.conf.timezone = 'UTC'
