# Generated by Django 3.2.5 on 2021-10-31 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_rename_grade_certexamrecord_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='index_number',
            field=models.CharField(help_text='Examination number', max_length=20),
        ),
    ]
