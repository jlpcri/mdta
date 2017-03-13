from django.contrib import admin

from .models import TestRailInstance, TestRailConfiguration, Project, Module, CatalogItem, ProjectVariable, Language, VUID


@admin.register(TestRailInstance, TestRailConfiguration, Project, Module, CatalogItem, ProjectVariable, Language, VUID)
class ProjectsAdmin(admin.ModelAdmin):
    pass
