from django.conf.urls import url, include
from rest_framework import routers

from . import views

urlpatterns = [
    url(r'^upload$', views.upload),
    url(r'^sigin_cert$', views.sigin_cert),
    url(r'^download$', views.download),
]