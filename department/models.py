from django.db import models
from django.shortcuts import reverse

from faculty.models import Faculty, auto_slug_faculty
from accounts.models import User


def upload_picture_to(instance, filename):
    import os
    new_filename = instance.name + os.path.splitext(filename)[-1]
    if instance.faculty:
        return os.path.join('faculty', instance.faculty.name, 'department', new_filename)
    return os.path.join('nonfacultydepartment', instance.name, new_filename)


class DepartmentManager(models.Manager):
    def get_for_faculty(self, faculty_slug, query=None):
        if query:
            return self.filter(faculty__slug=faculty_slug, name__icontains=query)
        return self.filter(faculty__slug=faculty_slug)

    def search(self, name):
        if name:
            return self.filter(name__icontains=name)
        else:
            return self.all()


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
    picture = models.ImageField(null=True, blank=True, upload_to=upload_picture_to)
    objects = DepartmentManager()

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

    def programmes(self):
        from programme.models import Programme
        return Programme.objects.filter(department_id=self.id)


models.signals.pre_save.connect(auto_slug_faculty, sender=Department)
