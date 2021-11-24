# Generated by Django 3.2.9 on 2021-11-19 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_alter_studentprogrammechoice_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentpreviouseducation',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='previous_education', related_query_name='previous_education', to='student.student'),
        ),
    ]
