from django.db import models
from django.shortcuts import reverse

from system.models import SemesterAcademicYearModel, Level
from accounts.models import User
from programme.models import Programme
from CollegeManagementSystem.validation import validate_alphanumberic_space
from ckeditor.fields import RichTextField
from lecture.models import Lecturer


class CourseManager(models.Manager):
    def get_for_programme(self, programme_id):
        return self.filter(programme_id=programme_id)


class Course(models.Model):
    name = models.CharField(max_length=120, unique=True, validators=[validate_alphanumberic_space])
    code = models.CharField(max_length=30, unique=True, validators=[validate_alphanumberic_space],
                            help_text='Course Code')
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, related_name='course_programme')
    created_by = models.ForeignKey(on_delete=models.CASCADE, to=User)
    semester = models.ForeignKey(SemesterAcademicYearModel, related_name='course_semester', on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='course_level')
    credit_hours = models.IntegerField()
    description = RichTextField(null=True, blank=True)
    updated_at = models.DateTimeField(help_text='Last modified', auto_now_add=True)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='course_lecturer')
    objects = CourseManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Course:detail', kwargs={
            'id': self.id,
            'code': self.code,
        })

    class Meta:
        order_with_respect_to = 'programme'
