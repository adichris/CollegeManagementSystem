# Generated by Django 3.2.9 on 2021-12-04 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_studentleveltotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='index',
            field=models.IntegerField(help_text='Index of the level start by 1 for the first level, 2 for next. etc', null=True, unique=True),
        ),
    ]