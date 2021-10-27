from django.db import models

from department.models import Department, auto_slug_faculty


class Programme(models.Model):
    name = models.CharField(max_length=200)
    department = models.ForeignKey(on_delete=models.CASCADE, to=Department, related_name='department',
                                   help_text='programmes\'s department')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name', 'id')
        db_table = 'programme'

models.signals.pre_save.connect(auto_slug_faculty, sender=Programme)
