# Generated by Django 4.0.2 on 2022-03-15 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empoymentHistory', '0006_alter_employmenthistorymodel_company_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employmenthistorymodel',
            options={'permissions': [('view_own_history', 'Can view their employment History')], 'verbose_name_plural': 'Employment Histories'},
        ),
    ]
