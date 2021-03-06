# Generated by Django 4.0 on 2022-02-13 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0019_alter_studentforms_academic_year'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentforms',
            options={'permissions': [('can_audit_admission_form', 'can audit student admission form'), ('can_reject_studentform', 'can reject student admission form'), ('can_accept_studentform', 'can accept student admission form'), ('view_studentform_detail', 'view student admission form detail'), ('view_own_forms', 'Can student view their own admission form detail')], 'verbose_name_plural': 'Student Forms'},
        ),
    ]
