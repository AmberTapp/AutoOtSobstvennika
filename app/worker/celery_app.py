
from celery import Celery
import os

celery = Celery("carbot", broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))
celery.conf.task_routes = {"app.worker.tasks.*": {"queue": "default"}}
