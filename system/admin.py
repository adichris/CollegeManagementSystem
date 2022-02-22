from django.contrib import admin
from .models import SemesterAcademicYearModel, Level


@admin.register(SemesterAcademicYearModel)
class SemesterModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'academic_year', 'is_current', 'timestamp')
    list_filter = ('is_current', )
    readonly_fields = ('is_current', )


@admin.register(Level)
class LevelModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
