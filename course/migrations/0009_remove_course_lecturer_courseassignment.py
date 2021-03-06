# Generated by Django 4.0.2 on 2022-03-16 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lecture', '0008_alter_lecturer_profile'),
        ('course', '0008_alter_course_order_with_respect_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='lecturer',
        ),
        migrations.CreateModel(
            name='CourseAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('is_tutor', models.BooleanField(default=False, help_text='Is the lecturer currently handling this course')),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.lecturer')),
            ],
            options={
                'unique_together': {('course', 'lecturer', 'is_tutor')},
            },
        ),
    ]
