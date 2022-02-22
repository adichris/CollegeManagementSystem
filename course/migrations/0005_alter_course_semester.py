# Generated by Django 4.0 on 2022-02-21 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_semesteracademicyearmodel'),
        ('course', '0004_course_lecturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_semester', to='system.semesteracademicyearmodel'),
        ),
    ]
