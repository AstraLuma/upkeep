from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from .views import stuffindex, thing, AddThing

urlpatterns = [
    url('^thing$', stuffindex, name='index'),
    url(r'^thing/(\d+)$', thing, name='thing'),
    url(r'^thing/add$', AddThing.as_view(), name='addthing'),
]
