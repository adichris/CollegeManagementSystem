from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from department.models import Department
from django.utils.timezone import now as today_time


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
                                   help_text=_('programmes\'s department'))
    slug = models.SlugField(unique=True)
    max_student = models.IntegerField(null=True,
                                      help_text=_('The maximum student this programme can take for a particular level'))
    objects = ProgrammeManager()

    def __str__(self):
        return self.name

    class Meta:
        order_with_respect_to = 'department'
        db_table = 'programme'
        permissions = [
            ('list_programme', _('can view programme list'))
        ]

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

    def count_new_student(self):
        return self.student_set.filter(date_admitted__year=today_time().year).count()

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
