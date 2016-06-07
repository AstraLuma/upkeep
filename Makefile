.PHONY: start_uwsgi
start_uwsgi:
	uwsgi --uid www --socket /var/www/uwsgi.sock --module upkeep.wsgi

.PHONY: start_worker
start_worker:
	./manage.py celery worker

.PHONY: sync
sync:
	git pull
	./manage.py migrate
	./manage.py collectstatic --noinput
	./manage.py installtasks

.PHONY: bounce-web
bounce-web:
	@echo "Bouncing application server"
	-service upkeep-web stop
	service upkeep-web start

.PHONY: bounce-job
bounce-job:
	@echo "Bouncing job worker"
	-service upkeep-job stop
	service upkeep-job start

.PHONY: update
update: sync bounce-web bounce-job
