This is a Django-based webapp for keeping track of maintenance of your stuff.

Daemons to setup:
* Main app (Django standard through wsgi, FastCGI, etc)
* RabbitMQ
* One or more Celery workers (start each with `./manage.py celery worker`)

Setup
=====
Create `upkeep/local_settings.py` and configure the following things:

* `SECRET_KEY`
* `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` & `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` ([Google API Console](https://console.developers.google.com/apis/credentials))
* `SOCIAL_AUTH_TWITTER_KEY` & `SOCIAL_AUTH_TWITTER_SECRET` ([Twitter Apps](http://twitter.com/apps/new))
* `SOCIAL_AUTH_FACEBOOK_KEY` & `SOCIAL_AUTH_FACEBOOK_SECRET` # ([Facebook Developers](https://developers.facebook.com/apps/))
* `BROKER_URL` (Your RabbitMQ instance for Celery)

You will probably find it useful to set these as well:
* `ALLOWED_HOSTS`
* `STATIC_ROOT`
* `DATABASES`
