from django.db import models
from django.conf import settings

class PushRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pushurl = models.URLField()
    added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pushurl')

    def __str__(self):
        return self.pushurl
