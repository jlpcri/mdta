from django.contrib import admin

from .models import Project, Module, CatalogItem


@admin.register(Project, Module, CatalogItem)
class ProjectsAdmin(admin.ModelAdmin):
    pass
