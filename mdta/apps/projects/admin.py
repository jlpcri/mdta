from django.contrib import admin

from .models import TestRailInstance, TestRailConfiguration,\
    Project, Module, CatalogItem, Language, VUID,\
    ProjectDatabaseSet, ProjectVariable


@admin.register(TestRailInstance, TestRailConfiguration,
                Project, Module, CatalogItem, Language, VUID,
                ProjectDatabaseSet, ProjectVariable)
class ProjectsAdmin(admin.ModelAdmin):
    pass
