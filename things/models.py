from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms import ModelForm

class Thing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('things:thing', args=[self.id])

class ThingForm(ModelForm):
    class Meta:
        model = Thing
        fields = ['name']


class Schedule(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    period = models.IntegerField()
    next_job_at = models.DateTimeField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('things.views.schedule', args=[self.id])

class Job(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    when = models.DateTimeField()
    done = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('things.views.job', args=[self.id])
