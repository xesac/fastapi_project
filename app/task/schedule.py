from app.task.celery_app import celery


@celery.task(name='period_task')
def period_task():
    print(12345)


