import kronos
import datetime
from django.core.management.base import NoArgsCommand
from .models import Schedule, Job
from .tasks import newjobnotify

@kronos.register('0 0 * * *') # Every day at 0:00
def create_jobs():
    q = Schedule.objects.filter(next_job_at__lte=datetime.date.today()).exclude(job__done=False)
    for sched in q:
        j = Job()
        j.schedule = sched
        j.when = datetime.date.today()
        j.done = False
        j.save()
        newjobnotify.delay(j.pk)

#@kronos.register('0 0 0 0 0')
def retry():
	j = Job.objects.order_by('-when')[0]
	print(j)
	newjobnotify.delay(j.pk)