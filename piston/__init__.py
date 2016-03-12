import requests

def notify(user):
	from .models import PushRegistration
	for pr in PushRegistration.objects.filter(user=user):
		requests.post(pr.pushurl)
