A basic wrapper around the Celery task queue.

This will automatically and load `task.py` files in the installed apps, and any callable registered with the `tasks.task` decorator will be registered with Celery.

(`tasks.get_celery()` will get you the Celery instance, if you need it.)