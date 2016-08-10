from django.conf.urls import url

from mdta.apps.testcases import views

urlpatterns = [
    url(r'^testcases/$', views.testcases, name='testcases'),
    url(r'^create_testcases/(?P<object_id>\d+)/$', views.create_testcases, name='create_testcases'),
    url(r'^push_testcases_to_testrail/(?P<project_id>\d+)/$', views.push_testcases_to_testrail, name='push_testcases_to_testrail'),

]
