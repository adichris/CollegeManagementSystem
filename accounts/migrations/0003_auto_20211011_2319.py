# Generated by Django 3.2.5 on 2021-10-11 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('t', 'Transgender'), ('o', 'Other')], max_length=5, null=True),
        ),
    ]
