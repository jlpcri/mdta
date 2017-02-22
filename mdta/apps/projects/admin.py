from django.contrib import admin

from .models import TestRailInstance, TestRailConfiguration, Project, Module, CatalogItem, ProjectVariable, Language


@admin.register(TestRailInstance, TestRailConfiguration, Project, Module, CatalogItem, ProjectVariable, Language)
class ProjectsAdmin(admin.ModelAdmin):
    pass
