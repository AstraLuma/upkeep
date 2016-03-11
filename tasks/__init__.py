import celery
import importlib
from django.conf import settings

_queue = None

def get_celery():
    global _queue
    modexists = lambda n: importlib.util.find_spec(n) is not None
    if _queue is None:
        _queue = celery.Celery('upkeep', # Project name
            broker=settings.BROKER_URL,
            )
        _queue.config_from_object(settings)
        _queue.autodiscover_tasks(settings.INSTALLED_APPS)
    return _queue

def task(callable):
    return get_celery().task(callable)
