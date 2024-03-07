from celery import Celery
from celery.schedules import crontab

from app.config.config import settings

celery = Celery(
    'tasks',
    broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
    include=[
        'app.task.tasks', 
        'app.task.schedule'
    ]
)


celery.conf.beat_schedule = {
    'hello': {'task': 'period_task',
            'schedule': 5} #секунды
        
}

