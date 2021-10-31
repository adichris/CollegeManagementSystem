from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.shortcuts import reverse

from department.models import Department


class ProgrammeManager(models.Manager):
    def search(self, name):
        if name:
            return self.filter(name__icontains=name)
        else:
            return self.all()

    def get_for_student_choices(self):
        return self.order_by('department__name', 'name')


class Programme(models.Model):
    name = models.CharField(max_length=200, unique=True)
    department = models.ForeignKey(on_delete=models.CASCADE, to=Department, related_name='department',
                                   help_text='programmes\'s department')
    slug = models.SlugField(unique=True)
    objects = ProgrammeManager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', 'id')
        db_table = 'programme'

    def get_absolute_url(self):
        return reverse(
            'Department:Programme:detail',
            kwargs={
                'slug': self.slug,
            }
        )

    def get_absolute_update_url(self):
        return reverse(
            'Department:Programme:update',
            kwargs={
                'slug': self.slug,
            }
        )

    def get_absolute_delete_url(self):
        return reverse(
            'Department:Programme:delete',
            kwargs={
                'slug': self.slug,
            }
        )


@receiver(models.signals.pre_save, sender=Programme)
def auto_slug_faculty(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
