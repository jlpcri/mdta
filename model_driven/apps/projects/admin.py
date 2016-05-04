from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    pass
