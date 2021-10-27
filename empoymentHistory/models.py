from django.db import models
from accounts.models import User
from ckeditor.fields import RichTextField


class EmploymentHistoryModel(models.Model):
    has_history = models.BooleanField(verbose_name='Do you have employment history', null=True,
                                      help_text='If you have no employment history uncheck this *.' )
    employee = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    company_name = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length=120, null=True, blank=True)
    state = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120, null=True, blank=True)
    specific_duty = RichTextField(verbose_name='Specific duties', null=True, blank=True)
    job_title = models.CharField(max_length=120, null=True, blank=True)
    supervisor = models.CharField(max_length=120, null=True, blank=True)
    employed_from = models.DateField(null=True, blank=True)
    employed_to = models.DateField(null=True, blank=True)
    why_leave = models.CharField(max_length=120, null=True, blank=True, help_text='Reason for leaving employment')

    class Meta:
        verbose_name_plural = 'Employment Histories'
        db_table = 'employmentHistory'
