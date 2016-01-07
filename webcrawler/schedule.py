from celery.schedules import crontab


CELERYBEAT_SCHEDULE = {
    'run_crawler_schedule': {
        'task': 'crawler.tasks.run_crawler',
        'schedule': crontab(minute=0, hour='*/12'),
    },
    'update_dictionary_schedule': {
        'task': 'crawler.tasks.update_dictionary',
        'schedule': crontab(minute=30, hour='*/1'),
    }
}
