from django.conf.urls import url

from mdta.apps.graphs import views

urlpatterns = [
    url(r'^$', views.graphs, name='graphs'),
    url(r'^node_type_new/$', views.node_type_new, name='node_type_new'),
    url(r'^node_type_edit/$', views.node_type_edit, name='node_type_edit'),
    url(r'^(?P<project_id>\d+)/node_new/$', views.project_new_node, name='project_new_node'),

    url(r'^edge_type_new/$', views.edge_type_new, name='edge_type_new'),
    url(r'^edge_type_edit/$', views.edge_type_edit, name='edge_type_edit'),
    url(r'^(?P<project_id>\d+)/edge_new/$', views.project_new_edge, name='project_new_edge'),

    url(r'^project_detail/(?P<project_id>\d+)/$', views.project_detail, name='project_detail'),

    url(r'^module_detail/(?P<module_id>\d+)/$', views.module_detail, name='module_detail'),
    url(r'^(?P<project_id>\d+)/module_new/$', views.module_new, name='module_new'),
    url(r'^(?P<project_id>\d+)/module_edit/$', views.module_edit, name='module_edit'),

    url(r'^get_keys_from_type/$', views.get_keys_from_type, name='get_keys_from_type'),

]
