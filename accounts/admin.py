from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class PersonAdmin(admin.ModelAdmin):
    pass
