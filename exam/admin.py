from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Question


@admin.register(Question)
class PersonAdmin(ImportExportModelAdmin):
    pass

