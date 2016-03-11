from tasks import task
from .models import Job

@task
def newjobnotify(jid):
	job = Job.objects.get(pk=jid)
	if job.done:
		return
	print(job)