from django.db import models
from ckeditor.fields import RichTextField
from django.dispatch import receiver
from django.utils.text import slugify
from django.shortcuts import reverse
from CollegeManagementSystem import validation


def upload_picture_to(instance, filename):
    import os
    new_filename = 'picture' + os.path.splitext(filename)[-1]
    return os.path.join('faculty', instance.name, new_filename)


def upload_icon_to(instance, filename):
    import os
    new_filename = 'icon' + os.path.splitext(filename)[-1]
    return os.path.join('faculty', instance.name, new_filename)


class FacultyManager(models.Manager):
    def search(self, query: str):
        if query:
            return self.filter(
                name__icontains=query,
            )
        else:
            return self.all()


class Faculty(models.Model):
    name = models.CharField(max_length=120, unique=True, validators=(validation.validate_alphanumberic_space,),
                            help_text='Name of Faculty,College, or School'
                            )
    slug = models.SlugField(unique=True)
    icon = models.ImageField(help_text='Faculty icon', upload_to=upload_icon_to)
    picture = models.ImageField(help_text='Picture of the faculty building, student , etc.', upload_to=upload_picture_to)
    note = RichTextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = FacultyManager()

    class Meta:
        db_table = 'faculty'
        verbose_name_plural = 'Faculties'
        verbose_name = 'Faculty'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('Faculty:detail',
                       kwargs={
                        "slug": self.slug
                       })

    def get_absolute_change_url(self):
        return reverse('Faculty:change',
                       kwargs={
                        "slug": self.slug
                       })

    def get_absolute_delete_url(self):
        return reverse('Faculty:delete',
                       kwargs={
                        "slug": self.slug
                       })


@receiver(models.signals.pre_save, sender=Faculty)
def auto_slug_faculty(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
