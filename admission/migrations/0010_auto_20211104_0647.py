# Generated by Django 3.2.5 on 2021-11-04 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0009_alter_studentforms_candidate_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentforms',
            name='is_current',
            field=models.BooleanField(default=True, help_text='Current status of the form.'),
        ),
        migrations.AlterField(
            model_name='studentforms',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('at profile', 'At Profile'), ('at address', 'At Address'), ('at certification', 'At Certification'), ('at employment', 'At Employment History'), ('at sponsor', 'AT SPONSORSHIP'), ('at programme', 'AT PROGRAMME'), ('at education', 'AT EDUCATION'), ('to detail', 'TO DETAIL'), ('expired', 'Expired'), ('new', 'New'), ('processing', 'Processing'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='new', max_length=30, null=True),
        ),
    ]
