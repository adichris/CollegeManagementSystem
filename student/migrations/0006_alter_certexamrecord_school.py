# Generated by Django 3.2.5 on 2021-10-30 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_admissioncertificate_certexamrecord'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='school',
            field=models.CharField(blank=True, help_text='School Name', max_length=200, null=True),
        ),
    ]
