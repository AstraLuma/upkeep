from tasks import task
from .models import Job
from piston import notify

@task
def newjobnotify(jid):
	try:
		job = Job.objects.get(pk=jid)
	except Job.DoesNotExit:
		return
	if job.done:
		return
	notify(job.schedule.thing.user)