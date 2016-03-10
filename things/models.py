from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

class ThingQuerySet(models.QuerySet):
    def accessible_by(self, user):
        if user.is_superuser:
            return self
        else:
            return self.filter(user=user)

class ThingManager(models.Manager):
    def get_queryset(self):
        return ThingQuerySet(self.model, using=self._db)

    def accessible_by(self, user):
        return self.get_queryset().accessible_by(user)

class Thing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    class Meta:
        unique_together = ('user', 'name',)

    objects = ThingManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('things:thing', args=[self.id])


class ScheduleQuerySet(models.QuerySet):
    def accessible_by(self, user):
        if user.is_superuser:
            return self
        else:
            return self.filter(thing__user=user)

class ScheduleManager(models.Manager):
    def get_queryset(self):
        return ScheduleQuerySet(self.model, using=self._db)

    def accessible_by(self, user):
        return self.get_queryset().accessible_by(user)

class Schedule(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    period = models.DurationField()
    next_job_at = models.DateField()

    class Meta:
        unique_together = ('thing', 'name',)

    objects = ScheduleManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('things.views.schedule', args=[self.id])


class JobQuerySet(models.QuerySet):
    def accessible_by(self, user):
        if user.is_superuser:
            return self
        else:
            return self.filter(schedule__thing__user=user)

class JobManager(models.Manager):
    def get_queryset(self):
        return ScheduleQuerySet(self.model, using=self._db)

    def accessible_by(self, user):
        return self.get_queryset().accessible_by(user)

class Job(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    when = models.DateField()
    done = models.BooleanField(default=False)
    # TODO: Only one undone job per schedule

    objects = JobManager()

    def __str__(self):
        if self.done:
            return "{} at {} (done)".format(self.schedule, self.when)
        else:
            return "{} at {}".format(self.schedule, self.when)

    def get_absolute_url(self):
        return reverse('things.views.job', args=[self.id])
