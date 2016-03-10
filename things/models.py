from django.db import models
from django.conf import settings

class Thing(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	name = models.CharField(max_length=128)

class Schedule(models.Model):
	thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
	name = models.CharField(max_length=128)
	period = models.IntegerField()
	next_job_at = models.DateTimeField()

class Job(models.Model):
	schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
	when = models.DateTimeField()
	done = models.BooleanField(default=True)
