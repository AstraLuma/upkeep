from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from .views import IndexView

urlpatterns = [
    url('^$', IndexView.as_view(), name='index'),
]
