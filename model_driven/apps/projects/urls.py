from django.conf.urls import url

from model_driven.apps.projects import views

urlpatterns = [
    url(r'^$', views.projects, name='projects'),
    url(r'^new/$', views.project_new, name='project_new'),
    url(r'^edit/$', views.project_edit, name='project_edit'),

    url(r'^module_new/$', views.module_new, name='module_new'),
    url(r'^module_edit/$', views.module_edit, name='module_edit'),

    url(r'^fetch_project_members', views.fetch_project_members, name='fetch_project_members'),

]
