from django.contrib import admin

from .models import TestServers, TestRun, AutomatedTestCase


@admin.register(TestServers, TestRun, AutomatedTestCase)
class RunnerAdmin(admin.ModelAdmin):
    pass
