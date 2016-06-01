from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from .views import (
	stuffindex, thing, AddThing, AddSchedule, 
	undones_json, finishjob_json, deletething_json, deleteschedule_json
	)

urlpatterns = [
    url('^thing$', stuffindex, name='index'),
    url(r'^thing/add$', AddThing.as_view(), name='addthing'),
    url(r'^thing/(\d+)$', thing, name='thing'),
    url(r'^thing/(\d+)/add$', AddSchedule.as_view(), name='addschedule'),
    url(r'^undones\.json', undones_json, name='undones.json'),
    url(r'^finish\.json', finishjob_json, name="finishjob.json"),
    url(r'^delete-thing\.json', deletething_json, name="delete-thing.json"),
    url(r'^delete-schedule\.json', deleteschedule_json, name="delete-schedule.json"),
]
