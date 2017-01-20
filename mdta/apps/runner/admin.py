from django.contrib import admin

from .models import TestServer


@admin.register(TestServer)
class RunnerAdmin(admin.ModelAdmin):
    pass
