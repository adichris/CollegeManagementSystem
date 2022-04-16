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

    def search(self, name=None, code=None, programme_name=None, name_start=None):
        return self.filter(
            name__icontains=name,
            name__istartswith=name_start,
            programme__name__icontains=programme_name,
            code__icontains=code
        )

    def search_by_name_code(self, query, **kwargs):
        return self.filter(models.Q(name__icontains=query) | models.Q(code__icontains=query), **kwargs)


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
    # lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, null=True, blank=True,
    #                              related_name='course_lecturer')
    objects = CourseManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Course:detail', kwargs={
            'id': self.id,
            'code': self.code,
        })

    @property
    def lecturer(self):
        try:
            lecturer = self.courseassignment_set.filter(is_tutor=True).first()
            if lecturer:
                return lecturer.lecturer
        except models.ObjectDoesNotExist:
            return

    class Meta:
        # order_with_respect_to = 'level'
        permissions = [
            ('view_courses_list', 'view courses list'),
            ('view_lecturer_details', 'Can lecturer view their course details'),
        ]

    def get_course_detail_4student_url(self):
        return reverse('Course:stu_details', kwargs={'course_code': self.code})


class CourseAssignment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, unique=False)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    is_tutor = models.BooleanField(default=False, help_text='Is the lecturer currently handling this course')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['lecturer', 'course', 'is_tutor'],
                                    condition=models.Q(is_tutor=True),
                                    name='unique_course_tutor'),
            models.UniqueConstraint(fields=['course', 'lecturer'],
                                    name='unique_course_lecturer')
        ]

    def __str__(self):
        return self.course.name + ' to ' + self.lecturer.profile.get_full_name()

    def get_absolute_update_url(self):
        return reverse('Course:assign_update', kwargs={
            'courseassignmentpk': self.pk
        })
