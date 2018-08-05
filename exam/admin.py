from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Question, Theory, TheoryTheme


@admin.register(Question)
class PersonAdmin(ImportExportModelAdmin):
    pass


@admin.register(Theory)
class PersonAdmin(ImportExportModelAdmin):
    pass


@admin.register(TheoryTheme)
class PersonAdmin(ImportExportModelAdmin):
    pass