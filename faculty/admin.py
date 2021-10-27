from django.contrib import admin

from .models import Faculty


@admin.register(Faculty)
class FacultyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp')
    readonly_fields = ('slug', )
