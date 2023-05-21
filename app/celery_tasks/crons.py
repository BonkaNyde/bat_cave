from celery.schedules import crontab, solar

beats = {
    'add_two': {
        'task': 'app.celery_tasks.tasks.add_two',
        'schedule': crontab('/every 15')
    },
    'every_morning_nairobi': {
        'task': 'app.celery_tasks.tasks.add_two',
        'schedule': solar('sunrise', 41.0082, 28.9784)
    }
}