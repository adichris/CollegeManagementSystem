from django.db import models
from department.models import Department
from accounts.models import User
from empoymentHistory.models import EmploymentHistoryModel
# Create your models here.
import os


class LecturerManager(models.Manager):
    def all(self):
        return self.filter(is_active=True)

    def search(self, query, **kwargs):
        if not query:
            return self.filter(is_active=True, **kwargs)

        return self.filter(
            models.Q(identity__icontains=query) | \
            models.Q(course_lecturer__created_by__first_name__icontains=query) | \
            models.Q(profile__last_name__icontains=query) | \
            models.Q(profile__email__icontains=query),
            **kwargs
        )


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
    profile = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True, related_name='lecturer',
                                   help_text='Lecturer profile')
    is_active = models.BooleanField(False)
    application_letter = models.FileField(null=True, help_text='Application/Résumé letter in pdf format',
                                          upload_to=upload_application_letter)
    cv = models.FileField(null=True, help_text='Lecturers application Curriculum Vitae (CV) in pdf format',
                          verbose_name='Curriculum Vitae (CV)', upload_to=upload_cv
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
        return self.profile.get_full_name() + ' : ' + self.identity

    def get_absolute_url(self):
        pass
        """Return absolute url for Lecturer."""
        # return ('')

    def courses(self):
        from course.models import Course
        return Course.objects.filter(courseassignment__lecturer=self, courseassignment__is_tutor=True)

    # TODO: Define custom methods here

    def slug(self):
        return self.profile.slug