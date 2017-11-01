from django.conf.urls import url


from mdta.apps.projects import views_dbset


urlpatterns = [
   url(r'^dbset/(?P<project_id>\d+)/dbset_db_new/$', views_dbset.project_dbset_db_new, name='project_dbset_db_new'),
   url(r'^dbset/dbset_db_edit/$', views_dbset.project_dbset_db_edit, name='project_dbset_db_edit'),

]
