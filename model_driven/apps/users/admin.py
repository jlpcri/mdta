from django.contrib import admin

from model_driven.apps.users.models import HumanResource


@admin.register(HumanResource)
class UsersAdmin(admin.ModelAdmin):
    pass
