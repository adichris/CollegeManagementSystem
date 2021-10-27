# Generated by Django 3.2.5 on 2021-10-19 06:09

import accounts.models
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211011_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('m', '♂️ Male'), ('f', '♀️ Female'), ('t', '⚧️ Transgender'), ('o', 'Other ')], max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(help_text='last name and other names', max_length=120),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(help_text='international phone number', max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(help_text='passport picture with white background', upload_to=accounts.models.upload_user_to_path),
        ),
    ]
