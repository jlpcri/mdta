from django.conf.urls import url

from mdta.apps.testcases import views

urlpatterns = [
    url(r'^create_testcases/(?P<object_id>\d+)/$', views.create_testcases, name='create_testcases'),

]
