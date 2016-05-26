from django.conf.urls import url

from mdta.apps.help import views

urlpatterns = [
    url(r'^$', views.help, name='help'),

]
