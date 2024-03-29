# Generated by Django 4.0.2 on 2022-05-02 15:29

import course.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_alter_courseassignment_managers_course_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='picture',
            field=models.ImageField(blank=True, help_text='Course picture or logo', null=True, upload_to=course.models.upload_course_picture_path),
        ),
    ]
