# Generated by Django 3.2.5 on 2021-10-17 17:24

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FormTypeChoicesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentForms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=120)),
                ('pin_code', models.CharField(max_length=120)),
                ('cost', models.IntegerField(blank=True, null=True)),
                ('candidate_name', models.CharField(max_length=120)),
                ('candidate_phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('sales_point', models.CharField(max_length=120)),
                ('sales_point_location', models.CharField(help_text='Town, city or community', max_length=120)),
                ('sales_agent', models.CharField(max_length=120, verbose_name="Sales agent's")),
                ('academic_year', models.CharField(help_text='this_year / next_year', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('form_type', models.ForeignKey(max_length=60, on_delete=django.db.models.deletion.CASCADE, related_name='form_type', to='admission.formtypechoicesmodel')),
            ],
            options={
                'unique_together': {('serial_number', 'pin_code')},
            },
        ),
        migrations.CreateModel(
            name='SalesOfAdmissionForms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity', models.CharField(blank=True, help_text='ID.', max_length=120, null=True)),
                ('received_from', models.CharField(help_text="payer's name", max_length=120)),
                ('amount', models.FloatField(help_text='amount paying')),
                ('the_sum_of', models.TextField(help_text='amount in words')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('signature', models.CharField(max_length=120)),
                ('admission_form', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='admission_form', to='admission.studentforms')),
            ],
        ),
    ]
