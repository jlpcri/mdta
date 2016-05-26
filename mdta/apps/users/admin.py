from django.contrib import admin

from mdta.apps.users.models import HumanResource


@admin.register(HumanResource)
class UsersAdmin(admin.ModelAdmin):
    pass
