from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    'run_crawler_schedule': {
        'task': 'crawler.tasks.run_crawler',
        'schedule': crontab(minute='*/3'),
    },
}
