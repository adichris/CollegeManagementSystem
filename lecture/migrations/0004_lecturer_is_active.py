# Generated by Django 3.2.9 on 2021-12-11 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0003_auto_20211211_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturer',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name=False),
            preserve_default=False,
        ),
    ]
