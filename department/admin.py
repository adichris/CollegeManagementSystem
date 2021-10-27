from django.contrib import admin

# Register your models here.
from .models import Department


@admin.register(Department)
class DepartmentModelAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'created_by')
    search_fields = ('name', 'short_form')
