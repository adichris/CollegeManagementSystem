from django.db import models

# Create your models here.


class ApplicantGrade(models.Model):
    letter = models.CharField(max_length=3, unique=True, null=False)
    value = models.IntegerField(default=1, help_text='Higher grade should have the highest number')

    def __str__(self):
        return self.letter
