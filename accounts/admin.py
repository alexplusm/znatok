from django.contrib import admin
from .models import Profile, Rank


@admin.register(Profile)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Rank)
class PersonAdmin(admin.ModelAdmin):
    pass
