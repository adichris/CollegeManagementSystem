# Generated by Django 4.0.2 on 2022-03-16 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0008_alter_lecturer_profile'),
        ('course', '0009_remove_course_lecturer_courseassignment'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='courseassignment',
            unique_together={('course', 'lecturer')},
        ),
    ]
