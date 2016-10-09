"""mdta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from mdta.apps.core.views import landing
from mdta.apps.graphs.views import home
from mdta.apps.users.views import intro

urlpatterns = [
    url(r'^mdta/$', landing, name='landing'),
    url(r'^mdta/intro/$', intro, name='intro'),
    url(r'^mdta/home/$', home, name='home'),
    url(r'^mdta/projects/', include('mdta.apps.projects.urls', namespace='projects')),
    url(r'^mdta/graphs/', include('mdta.apps.graphs.urls', namespace='graphs')),
    url(r'^mdta/users/', include('mdta.apps.users.urls', namespace='users')),
    url(r'mdta/help/', include('mdta.apps.help.urls', namespace='help')),
    url(r'mdta/testcases/', include('mdta.apps.testcases.urls', namespace='testcases')),

    url(r'^mdta/admin/', include(admin.site.urls)),
]
