from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'programme', 'semester', 'level', 'credit_hours')
    readonly_fields = ('programme',)
    search_fields = ('name', 'code', )
    list_filter = ('semester', 'level')
