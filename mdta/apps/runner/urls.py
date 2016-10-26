from django.conf.urls import url

from mdta.apps.runner import views

urlpatterns = [
    url(r'^demo/(?P<project_id>\d+)/$', views.demo, name='demo'),

]
