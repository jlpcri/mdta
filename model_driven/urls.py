"""model_driven URL Configuration

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
from django.conf.urls import url, include, patterns
from django.contrib import admin

from model_driven.apps.core.views import landing

urlpatterns = [
    url(r'^model_driven/$', landing, name='landing'),
    # url(r'^model_driven/projects/', include('model_driven.apps.projects.urls', namespace='projects')),
    url(r'^model_driven/users/', include('model_driven.apps.users.urls', namespace='users')),
    # url(r'model_driven/help/', include('model_driven.apps.help.urls', namespace='help')),

    url(r'^admin/', admin.site.urls),
]
