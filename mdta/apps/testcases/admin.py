from django.contrib import admin

from .models import TestCaseHistory


@admin.register(TestCaseHistory)
class ProjectsAdmin(admin.ModelAdmin):
    pass
