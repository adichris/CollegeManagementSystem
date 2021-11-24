# Generated by Django 3.2.9 on 2021-11-21 15:58

import CollegeManagementSystem.validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0015_auto_20211121_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentforms',
            name='candidate_name',
            field=models.CharField(blank=True, max_length=120, null=True, validators=[CollegeManagementSystem.validation.validate_alphanumberic_space]),
        ),
    ]
