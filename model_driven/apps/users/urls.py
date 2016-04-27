from django.conf.urls import url

from model_driven.apps.users import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^signin/$', views.sign_in, name='sign_in'),
    url(r'^signout/$', views.sign_out, name='sign_out'),
    url(r'^user_management/$', views.user_management, name='management'),

]
