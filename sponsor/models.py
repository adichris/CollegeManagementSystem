from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from student.models import Student
# Create your models here.


class StudentSponsor(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_sponsored', unique=True)
    name = models.CharField(help_text='Name of sponsor or company', verbose_name='Sponsor / Company', max_length=120)
    email = models.EmailField(help_text="Sponsor's email address")
    phone_number = PhoneNumberField(help_text="Sponsor's phone number", null=True, blank=True)
    city = models.CharField(max_length=120, help_text='Sponsor\'s city', null=True, blank=True)
    state = models.CharField(max_length=120, help_text='Sponsor\'s state', null=True, blank=True)
    address = models.CharField(help_text='Address of sponsor', max_length=120)
    relationship = models.CharField(help_text='Your relationship with the sponsor', null=True, max_length=120)
    scholarship = models.BooleanField(null=True)
    on_government_support = models.BooleanField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Student Sponsor'
        verbose_name_plural = 'Student Sponsors'
        db_table = 'studentSponsor'
