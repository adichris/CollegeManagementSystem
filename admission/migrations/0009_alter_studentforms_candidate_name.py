# Generated by Django 3.2.5 on 2021-10-22 04:35

import CollegeManagementSystem.validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0008_alter_studentforms_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentforms',
            name='candidate_name',
            field=models.CharField(max_length=120, null=True, validators=[CollegeManagementSystem.validation.validate_alphanumberic_space]),
        ),
    ]
