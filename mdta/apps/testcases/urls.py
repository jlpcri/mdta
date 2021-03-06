from django.conf.urls import url

from mdta.apps.testcases import views

urlpatterns = [
    url(r'^$', views.tcs_project, name='tcs_project'),

    url(r'^testcases/$', views.testcases, name='testcases'),
    url(r'^create_testcases/(?P<object_id>\d+)/$', views.create_testcases, name='create_testcases'),
    url(r'^create_testcases_all/$', views.create_testcases_all, name='create_testcases_all'),
    url(r'^demonstrate_testcases/(?P<object_id>\d+)/$', views.demonstrate_testcases, name='demonstrate_testcases'),

    url(r'^push_testcases_to_testrail/(?P<project_id>\d+)/$', views.push_testcases_to_testrail, name='push_testcases_to_testrail'),

    url(r'^testrail_configuration_new/$', views.testrail_configuration_new, name='testrail_configuration_new'),
    url(r'^testrail_configuration_delete/(?P<testrail_id>\d+)/$', views.testrail_configuration_delete, name='testrail_configuration_delete'),
    url(r'^testrail_configuration_update/(?P<testrail_id>\d+)/$', views.testrail_configuration_update, name='testrail_configuration_update'),

    url(r'^check_celery_task_state/$', views.check_celery_task_state, name='check_celery_task_state'),
    url(r'^check_edges_visited/(?P<project_id>\d+)', views.check_edges_visited, name='check_edges_visited'),
]
