from django.db import models
from django.utils.text import slugify
from django.dispatch import receiver
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from department.models import Department


class ProgrammeManager(models.Manager):
    def search(self, name):
        if name:
            return self.filter(name__icontains=name)
        else:
            return self.all()

    def get_for_student_choices(self):
        return self.order_by('department__name', 'name')


def programme_picture_path(instance, filename):
    import os
    programme_name = instance.name.replace(" ", "")
    return os.path.join(
        "programme",
        programme_name,
        programme_name[:20]+os.path.splitext(filename)[-1]
    )


class Programme(models.Model):
    picture = models.ImageField(null=True, blank=True, help_text="Department picture or logo", upload_to=programme_picture_path)
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
        return self.new_student().count()

    def new_student(self):
        from system.models import Level
        return self.student_set.filter(level=Level.objects.get_4first_year())

    @property
    def students(self):
        return self.student_set.filter(is_active=True, profile__is_active=True)

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
