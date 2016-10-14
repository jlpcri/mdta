from django.conf.urls import url

from mdta.apps.projects import views

urlpatterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'^project_dashboard', views.project_dashboard, name='project_dashboard'),
    url(r'^project_config/(?P<project_id>\d+)/$', views.project_config, name='project_config'),
    url(r'^new/$', views.project_new, name='project_new'),
    url(r'^edit/(?P<project_id>\d+)/$', views.project_edit, name='project_edit'),

    url(r'^module_new/$', views.module_new, name='module_new'),
    url(r'^module_edit/(?P<module_id>\d+)/$', views.module_edit, name='module_edit'),

    url(r'^test_header_new/$', views.test_header_new, name='test_header_new'),
    url(r'^test_header_edit/(?P<test_header_id>\d+)/$', views.test_header_edit, name='test_header_edit'),

    url(r'^fetch_project_catalogs_members', views.fetch_project_catalogs_members, name='fetch_project_catalogs_members'),

]
