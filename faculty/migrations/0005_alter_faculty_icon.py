# Generated by Django 3.2.5 on 2021-10-23 17:56

from django.db import migrations, models
import faculty.models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0004_auto_20211022_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='icon',
            field=models.ImageField(help_text='Faculty icon', upload_to=faculty.models.upload_icon_to),
        ),
    ]
