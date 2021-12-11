from django.db import models
from CollegeManagementSystem.validation import validate_alphanumberic_space
from django.shortcuts import reverse
from INSTITUTION.utils import AcademicYear
from programme.models import Programme
from django.utils.translation import gettext_lazy as  _
from django.dispatch import receiver


class SemesterModel(models.Model):
    name = models.CharField(max_length=60, help_text=_('Semester/term name. Eg. First Semester'), validators=[validate_alphanumberic_space], unique=True)
    timestamp = models.DateTimeField(auto_now=True)
    is_current = models.BooleanField(default=False, verbose_name=_('Current Semester'))

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


class LevelManager(models.Manager):
    def get_4first_year(self):
        level = self.filter(index=1)
        if level.exists():
            return level
        return self.first()


class Level(models.Model):
    name = models.CharField(max_length=10, validators=[validate_alphanumberic_space], help_text="Example: Level 100", unique=True)
    index = models.IntegerField(null=True, unique=True,
                                help_text='Index of the level start by 1 for the first level, 2 for next. etc')
    objects = LevelManager()

    def __str__(self):
        return self.name


@receiver(models.signals.post_save, sender=Level)
def auto_index_level(instance, created, **kwargs):
    if created and not instance.index:
        instance.index = Level.objects.count() + 1
        instance.save()


class StudentLevelTotal(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    current_number = models.IntegerField(help_text=_('Current number of student'))
    max_number = models.IntegerField(help_text=_('Maximum number of student'))
    academic_year = models.CharField(max_length=10, choices=AcademicYear.choices(), default=AcademicYear.default())
    programme = models.ForeignKey(Programme, related_name=_('student_lvl_total'), on_delete=models.CASCADE)

    def __str__(self):
        return self.current_number

    class Meta:
        db_table = 'studentleveltotal'
        order_with_respect_to = 'programme'
