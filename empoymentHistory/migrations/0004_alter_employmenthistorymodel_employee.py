# Generated by Django 3.2.5 on 2021-10-21 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('empoymentHistory', '0003_auto_20211020_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employmenthistorymodel',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
