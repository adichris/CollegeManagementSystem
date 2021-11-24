# Generated by Django 3.2.9 on 2021-11-21 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admission', '0013_alter_studentforms_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentforms',
            options={'permissions': [('can_audit_admission_form', 'can audit student admission form'), ('view_studentform_detail', 'view student admission form detail')], 'verbose_name_plural': 'Student Forms'},
        ),
        migrations.AlterField(
            model_name='studentforms',
            name='academic_year',
            field=models.CharField(choices=[('2020/2021', '2020/2021'), ('2019/2020', '2019/2020'), ('2018/2019', '2018/2019'), ('2017/2018', '2017/2018'), ('2016/2017', '2016/2017'), ('2015/2016', '2015/2016'), ('2014/2015', '2014/2015'), ('2013/2014', '2013/2014'), ('2012/2013', '2012/2013'), ('2011/2012', '2011/2012'), ('2010/2011', '2010/2011'), ('2009/2010', '2009/2010'), ('2008/2009', '2008/2009'), ('2007/2008', '2007/2008'), ('2006/2007', '2006/2007'), ('2005/2006', '2005/2006'), ('2004/2005', '2004/2005'), ('2003/2004', '2003/2004'), ('2002/2003', '2002/2003'), ('2001/2002', '2001/2002'), ('2000/2001', '2000/2001')], default=(2020, 2021), help_text='this_year / next_year', max_length=10, null=True),
        ),
    ]
