from django.contrib import admin

from .models import TestRailInstance, TestRailConfiguration, TestCaseResults


@admin.register(TestRailInstance, TestRailConfiguration, TestCaseResults)
class ProjectsAdmin(admin.ModelAdmin):
    pass
