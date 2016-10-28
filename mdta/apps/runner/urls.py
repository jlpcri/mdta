from django.conf.urls import url

from mdta.apps.runner import views

urlpatterns = [
    url(r'^demo/(?P<project_id>\d+)/$', views.demo, name='demo'),
    url(r'^suites/(?P<project_id>\d+)/$', views.display_project_suites, name='suites'),
    url(r'^steps/(?P<mdta_project_id>\d+)/$', views.display_testrail_steps, name='steps'),
    url(r'^run/(?P<mdta_project_id>\d+)/$', views.execute_test, name='run'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
]
