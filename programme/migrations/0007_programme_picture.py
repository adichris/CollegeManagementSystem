# Generated by Django 4.0.2 on 2022-05-02 15:29

from django.db import migrations, models
import programme.models


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0006_alter_programme_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='picture',
            field=models.ImageField(blank=True, help_text='Department picture or logo', null=True, upload_to=programme.models.programme_picture_path),
        ),
    ]
