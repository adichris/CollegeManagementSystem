from django.db import models
from django.shortcuts import reverse

from faculty.models import Faculty, auto_slug_faculty
from accounts.models import User


class Department(models.Model):
    faculty = models.ForeignKey(
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        to=Faculty,
        related_name='faculty',
        help_text='Department\'s faculty',
    )
    name = models.CharField(
        max_length=120,
        help_text='The name of the department.',
        unique=True,
    )
    short_form = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        unique=True,
        verbose_name='Short name',
        help_text='Department Abbreviation. Short name/form'
    )
    slug = models.SlugField(unique=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'department'
        verbose_name_plural = 'Departments'
        verbose_name = 'department'

    def __str__(self):
        return self.name

    @property
    def has_faculty(self):
        return bool(self.faculty)

    def get_absolute_url(self):
        return reverse('Department:detail', kwargs={
            'slug': self.slug
        })

    def get_absolute_update_url(self):
        return reverse('Department:update', kwargs={
            'slug': self.slug
        })

    def get_absolute_delete_url(self):
        return reverse('Department:delete', kwargs={
            'slug': self.slug
        })


models.signals.pre_save.connect(auto_slug_faculty, sender=Department)
