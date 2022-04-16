from django.contrib import admin
from .models import Course, CourseAssignment


@admin.register(Course)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'programme', 'semester', 'level', 'credit_hours')
    readonly_fields = ('programme',)
    search_fields = ('name', 'code', )
    list_filter = ('semester', 'level')


@admin.register(CourseAssignment)
class CourseAssignmentModelAdmin(admin.ModelAdmin):
    list_display = ('course', 'lecturer', 'is_tutor')
    readonly_fields = ('lecturer', 'course', 'assigned_by')
    search_fields = ('course',)
    list_filter = ('is_tutor', )
