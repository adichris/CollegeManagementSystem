from django.contrib import admin
from .models import (
    StudentProgrammeChoice,
    AdmissionCertificate,
    StudentPreviousEducation,
    CertExamRecord,
    Student
)


@admin.register(CertExamRecord)
class CertExamRecord(admin.ModelAdmin):
    list_display = ('certificate', 'index_number', 'subject', 'grade', 'school')
    readonly_fields = list_display + ('examination_year', 'examination_type')

    search_fields = ('index_number', )


@admin.register(StudentPreviousEducation)
class StudentPreviousEducationModelAdmin(admin.ModelAdmin):
    list_display = ('student', 'school', 'region', 'from_year', 'to_year')
    readonly_fields = list_display


@admin.register(AdmissionCertificate)
class AdmissionCertificateModelAdmin(admin.ModelAdmin):
    list_display = ('student', )
    readonly_fields = list_display + ('certificate_picture', )


@admin.register(StudentProgrammeChoice)
class StudentProgrammeChoiceModelAdmin(admin.ModelAdmin):
    list_display = ('student', 'first_choice', 'second_choice', 'third_choice')
    readonly_fields = list_display

    fieldsets = (
        ('Student', {'fields': ('student', )}),
        ('Choices', {'fields': ('first_choice', 'second_choice', 'third_choice')}),
    )


@admin.register(Student)
class StudentModelAdmin(admin.ModelAdmin):
    list_display = ('profile', 'admission_form', 'index_number', 'programme', 'date_admitted', 'is_active')
    readonly_fields = ('profile', 'admission_form', 'index_number', 'programme', 'date_admitted', )
    list_filter = ('is_active', )

    search_fields = ('index_number', )

    fieldsets = [
        ('Profile', {'fields': ('profile',)}),
        ('Admission Form', {'fields': ('admission_form',)}),
        ('Programme', {'fields': ('programme',)}),
        ('Date to Complete', {'fields': ('date_admitted', 'date_completed')}),
        ('Status', {'fields': ('is_active', )}),
    ]