from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from .views import addurl, dropurl, manifest

urlpatterns = [
    url(r'^register', addurl, name='register'),
    url(r'^unregister', dropurl, name='unregister'),
    url(r'^manifest\.json', manifest, name='manifest'),
]
