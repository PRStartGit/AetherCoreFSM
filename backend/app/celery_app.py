"""
Celery Application Configuration
"""
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "zynthio",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=['app.celery_tasks']
)

# Celery configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    result_expires=3600,  # 1 hour
)

# Celery Beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    'send-daily-reports': {
        'task': 'app.celery_tasks.send_daily_reports',
        'schedule': crontab(hour=9, minute=0),  # Run at 9:00 AM every day
    },
    'send-weekly-reports': {
        'task': 'app.celery_tasks.send_weekly_reports',
        'schedule': crontab(hour=9, minute=15),  # Run at 9:15 AM every day, check which sites need weekly reports
    },
    'generate-daily-checklists': {
        'task': 'app.celery_tasks.generate_daily_checklists',
        'schedule': crontab(hour=0, minute=1),  # Run at 00:01 every day
    },
}
