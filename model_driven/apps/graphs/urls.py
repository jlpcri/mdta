from django.conf.urls import url

from model_driven.apps.graphs import views

urlpatterns = [
    url(r'^$', views.graphs, name='graphs'),
    url(r'^node_type_new/$', views.node_type_new, name='node_type_new'),
    url(r'^node_type_edit/$', views.node_type_edit, name='node_type_edit'),
    url(r'^(?P<project_id>\d+)/node_new/$', views.node_new, name='node_new'),

    url(r'^edge_type_new/$', views.edge_type_new, name='edge_type_new'),
    url(r'^edge_type_edit/$', views.edge_type_edit, name='edge_type_edit'),

    url(r'^get_keys_from_type/$', views.get_keys_from_type, name='get_keys_from_type'),

]
