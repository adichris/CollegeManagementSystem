# Generated by Django 3.2.9 on 2021-11-23 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semestermodel',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
