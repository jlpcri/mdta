from django.contrib import admin

from .models import TestRailInstance, TestRailConfiguration, Project, Module, CatalogItem, ProjectVariable


@admin.register(TestRailInstance, TestRailConfiguration, Project, Module, CatalogItem, ProjectVariable)
class ProjectsAdmin(admin.ModelAdmin):
    pass
