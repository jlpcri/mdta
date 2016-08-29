from django.contrib import admin

from .models import TestRailInstance, TestRailConfiguration, Project, Module, CatalogItem


@admin.register(TestRailInstance, TestRailConfiguration, Project, Module, CatalogItem)
class ProjectsAdmin(admin.ModelAdmin):
    pass
