# Generated by Django 3.2.9 on 2021-12-17 01:15

from django.db import migrations, models
import lecture.models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0004_lecturer_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='cv',
            field=models.FileField(help_text='Lecturers application Curriculum Vitae (CV) in pdf format', null=True, upload_to=lecture.models.upload_cv, verbose_name='Curriculum Vitae (CV)'),
        ),
    ]
