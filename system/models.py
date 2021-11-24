from django.db import models
from CollegeManagementSystem.validation import validate_alphanumberic_space
from django.shortcuts import reverse
from INSTITUTION.utils import AcademicYear


class SemesterModel(models.Model):
    name = models.CharField(max_length=60, help_text='Semester/term name. Eg. First Semester', validators=[validate_alphanumberic_space], unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    is_current = models.BooleanField(default=False, verbose_name='Current Semester')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'institution_semester'
        verbose_name_plural = 'Semesters'
        verbose_name = 'Semester'
        constraints = [
            models.UniqueConstraint(
                fields=['is_current'],
                condition=models.Q(is_current=True),
                name='unique_active_semester'
            )
        ]

    def get_absolute_url(self):
        return reverse('System:semester_academic_year')

    def get_absolute_update_url(self):
        return reverse('System:semester_update',
                       kwargs={
                           'name': self.name,
                           'id': self.id
                       })


academic_year = AcademicYear()


class System(models.Model):
    current_academic_year = models.CharField(max_length=10, choices=academic_year.choices(), default=academic_year.default())
