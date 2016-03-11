from django.core.management.base import BaseCommand
from ... import get_celery

class Command(BaseCommand):
    help = "Starts a job queue worker"
    def add_arguments(self, parser):
        parser.add_argument('args', metavar='subcommand', nargs='*',
            help='Command to be passed to celery')

    def handle(self, *args, **kwargs):
        get_celery().start(['./manage.py celery'] + list(args))