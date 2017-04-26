from django.contrib import admin

from .models import TestServer, TestRun, AutomatedTestCase


@admin.register(TestServer, TestRun, AutomatedTestCase)
class RunnerAdmin(admin.ModelAdmin):
    pass
