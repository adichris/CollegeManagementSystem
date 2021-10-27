from django.contrib import admin

from .models import StudentSponsor


@admin.register(StudentSponsor)
class StudentSponsorModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'phone_number')
    readonly_fields = list_display + ('state', 'email', 'scholarship', 'on_government_support')
    search_fields = ('name', )
    list_filter = ('scholarship', 'on_government_support')
