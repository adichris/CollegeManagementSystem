# Generated by Django 3.2.5 on 2021-10-27 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0002_auto_20211027_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
