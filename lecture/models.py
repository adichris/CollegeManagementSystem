from django.db import models
from department.models import Department
from accounts.models import User
from empoymentHistory.models import EmploymentHistoryModel
# Create your models here.
import os


class LecturerManager(models.Manager):
    def all(self):
        return self.filter(is_active=True)


def upload_application_letter(instance, filename):
    lecturer_dir = str(instance.identity or instance.profile.email)
    return os.path.join('lecturer', lecturer_dir, 'application_letter', filename)


def upload_cv(instance, filename):
    lecturer_dir = str(instance.identity or instance.profile.email)
    return os.path.join('lecturer', lecturer_dir, 'cv', filename)


class Lecturer(models.Model):
    """Model definition for Lecturer."""
    identity = models.CharField(max_length=30, unique=True, blank=False, help_text='Lecturer identity')
    department = models.ForeignKey(null=True, to=Department, on_delete=models.CASCADE)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(False)
    application_letter = models.FileField(null=True, help_text='Application/Résumé letter in pdf format',
                                          upload_to=upload_application_letter)
    cv = models.FileField(null=True, help_text='Lecturers application Curriculum Vitae (CV) in pdf format',
                          verbose_name='Curriculum Vitae (CV)',
                          )
    objects = LecturerManager()

    class Meta:
        """Meta definition for Lecturer."""
        verbose_name = 'Lecturer'
        verbose_name_plural = 'Lecturers'
        permissions = [
            ('assign_department', 'Assign Department'),
            ('list_lecturer', 'view lecturers list'),
        ]

    def __str__(self):
        """Unicode representation of Lecturer."""
        return self.identity

    def get_absolute_url(self):
        pass
        """Return absolute url for Lecturer."""
        # return ('')

    def courses(self):
        return self.course_lecturer

    # TODO: Define custom methods here
