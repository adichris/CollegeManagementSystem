# Generated by Django 3.2.9 on 2021-12-01 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0026_alter_student_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='date_completed',
            field=models.DateField(blank=True, help_text='Date student will completed school', null=True),
        ),
    ]