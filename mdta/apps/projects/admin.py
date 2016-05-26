from django.contrib import admin

from .models import Project, Module, TestCaseHistory


@admin.register(Project, Module, TestCaseHistory)
class ProjectsAdmin(admin.ModelAdmin):
    pass
