from django.conf.urls import url

from mdta.apps.users import views

urlpatterns = [
    url(r'^mdta/$', views.mdta, name='mdta'),
    url(r'^signin/$', views.sign_in, name='sign_in'),
    url(r'^signout/$', views.sign_out, name='sign_out'),
    url(r'^user_management/$', views.user_management, name='management'),
    url(r'^user_update/(?P<user_id>\d+)/$', views.user_update, name='user_update'),

]
