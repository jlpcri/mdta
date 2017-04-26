from django.contrib import admin

from .models import TestServers


@admin.register(TestServers)
class RunnerAdmin(admin.ModelAdmin):
    pass
