from django.conf.urls import url

from mdta.apps.graphs import views

urlpatterns = [
    url(r'^$', views.graphs, name='graphs'),
    url(r'^node_type_new/$', views.node_type_new, name='node_type_new'),
    url(r'^node_type_edit/$', views.node_type_edit, name='node_type_edit'),
    url(r'^(?P<project_id>\d+)/project_node_new/$', views.project_node_new, name='project_node_new'),

    url(r'^edge_type_new/$', views.edge_type_new, name='edge_type_new'),
    url(r'^edge_type_edit/$', views.edge_type_edit, name='edge_type_edit'),
    url(r'^(?P<project_id>\d+)/project_edge_new/$', views.project_edge_new, name='project_edge_new'),

    url(r'^project_detail/(?P<project_id>\d+)/$', views.project_detail, name='project_detail'),

    url(r'^project_module_detail/(?P<module_id>\d+)/$', views.project_module_detail, name='project_module_detail'),
    url(r'^(?P<project_id>\d+)/project_module_new/$', views.project_module_new, name='project_module_new'),
    url(r'^(?P<project_id>\d+)/project_module_edit/$', views.project_module_edit, name='project_module_edit'),
    url(r'(?P<module_id>\d+)/module_node_new/$', views.module_node_new, name='module_node_new'),
    url(r'(?P<module_id>\d+)/module_node_edit/$', views.module_node_edit, name='module_node_edit'),
    url(r'(?P<module_id>\d+)/module_edge_new/$', views.module_edge_new, name='module_edge_new'),
    url(r'(?P<module_id>\d+)/module_edge_edit/$', views.module_edge_edit, name='module_edge_edit'),

    url(r'^get_keys_from_type/$', views.get_keys_from_type, name='get_keys_from_type'),
    url(r'^get_leaving_edges_from_node/$', views.get_leaving_edges_from_node, name='get_leaving_edges_from_node'),

]
