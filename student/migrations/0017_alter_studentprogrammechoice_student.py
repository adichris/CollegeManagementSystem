# Generated by Django 3.2.9 on 2021-11-19 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0016_alter_studentpreviouseducation_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentprogrammechoice',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='programme_choices', to='student.student'),
        ),
    ]
