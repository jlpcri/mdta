from django.conf.urls import url

from model_driven.apps.projects import views

urlpatterns = [
    url(r'^$', views.projects, name='projects'),

]
