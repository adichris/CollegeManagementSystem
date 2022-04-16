# Generated by Django 4.0.2 on 2022-03-03 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0043_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Auto Mechanics', 'Auto Mechanics'), ('Government', 'Government'), ('Chemistry', 'Chemistry'), ('Financial Accounting', 'Financial Accounting'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Literature-in English', 'Literature-in English'), ('English Language', 'English Language'), ('Technical Drawing', 'Technical Drawing'), ('Ceramics', 'Ceramics'), ('General Agriculture', 'General Agriculture'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('ICT (Elective)', 'ICT (Elective)'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Integrated Science', 'Integrated Science'), ('Basketry', 'Basketry'), ('Dagbani', 'Dagbani'), ('Social Studies', 'Social Studies'), ('French', 'French'), ('Physics', 'Physics'), ('Leatherwork', 'Leatherwork'), ('Ga', 'Ga'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Woodwork', 'Woodwork'), ('Jewellery', 'Jewellery'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Literature in English', 'Literature in English'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Graphic Design', 'Graphic Design'), ('Gonja', 'Gonja'), ('Languages', 'Languages'), ('Kasem', 'Kasem'), ('French OR Music', 'French OR Music'), ('Metalwork', 'Metalwork'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Fisheries', 'Fisheries'), ('Electronics', 'Electronics'), ('Music', 'Music'), ('Picture Making', 'Picture Making'), ('Nzema', 'Nzema'), ('Applied Electricity', 'Applied Electricity'), ('Ewe', 'Ewe'), ('Management-In-Living', 'Management-In-Living'), ('Business Management', 'Business Management'), ('Any one or two of the following', 'Any one or two of the following'), ('Geography', 'Geography'), ('Economics', 'Economics'), ('Textiles', 'Textiles'), ('Animal Husbandry', 'Animal Husbandry'), ('Dagaare', 'Dagaare'), ('Dangme', 'Dangme'), ('History', 'History'), ('Twi (Asante)', 'Twi (Asante)'), ('Sculpture', 'Sculpture'), ('Arabic', 'Arabic'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('French or Music', 'French or Music'), ('Forestry', 'Forestry'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Building Construction', 'Building Construction'), ('Biology', 'Biology')], max_length=120),
        ),
    ]