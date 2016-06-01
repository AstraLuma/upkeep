from tasks import task
from .models import Job
from piston import notify

@task
def newjobnotify(jid):
	try:
		job = Job.objects.get(pk=jid)
	except Job.DoesNotExist:
		return
	if job.done:
		return
	notify(job.schedule.thing.user, 
		text="You need to {} on your {}".format(job.schedule.name, job.schedule.thing.name),
		)