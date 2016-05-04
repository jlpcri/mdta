from django.conf.urls import url

from model_driven.apps.graphs import views

urlpatterns = [
    url(r'^$', views.graphs, name='graphs'),

]
