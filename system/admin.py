from django.contrib import admin
from .models import SemesterModel, Level


@admin.register(SemesterModel)
class SemesterModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp', 'is_current')
    list_filter = ('is_current', )
    readonly_fields = ('is_current', )


@admin.register(Level)
class LevelModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
