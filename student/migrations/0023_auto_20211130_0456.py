# Generated by Django 3.2.9 on 2021-11-30 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0022_auto_20211128_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='certificate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certificate_records', to='student.admissioncertificate'),
        ),
        migrations.AlterField(
            model_name='certexamrecord',
            name='grade',
            field=models.CharField(choices=[('A1', 'A1'), ('B2', 'B2'), ('C3', 'C3'), ('C4', 'C4'), ('C5', 'C5'), ('C6', 'C6'), ('D7', 'D7'), ('E8', 'E8'), ('F9', 'F9')], max_length=3),
        ),
    ]