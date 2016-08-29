from django.contrib import admin

from .models import TestCaseResults


@admin.register(TestCaseResults)
class ProjectsAdmin(admin.ModelAdmin):
    pass
