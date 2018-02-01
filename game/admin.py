from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import PickForMiniGame


@admin.register(PickForMiniGame)
class PersonAdmin(ImportExportModelAdmin):
    pass