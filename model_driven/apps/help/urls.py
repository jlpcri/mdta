from django.conf.urls import url

from model_driven.apps.help import views

urlpatterns = [
    url(r'^$', views.help, name='help'),

]
