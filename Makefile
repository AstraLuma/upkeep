.PHONY: start_uwsgi
start_uwsgi:
        uwsgi --uid www --socket /var/www/uwsgi.sock --module upkeep.wsgi

.PHONY: start_worker
start_worker:
        ./manage.py celery worker

.PHONY: update
update:
        git pull
        ./manage.py collectstatic --noinput
        ./manage.py installtasks
