# Generated by Django 3.2.9 on 2021-12-17 01:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0030_auto_20211205_1226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ('id', 'profile'), 'permissions': [('list_student', 'can view student list'), ('staff_view_student', 'can view student detail as staff')], 'verbose_name': 'Student', 'verbose_name_plural': 'Students'},
        ),
    ]
