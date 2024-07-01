from celery import Celery

celery = Celery(
    'tasks',
    broker=f'amqp://guest:guest@localhost:5672//',
    include=['app.tasks.tasks']
)
