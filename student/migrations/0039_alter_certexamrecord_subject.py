# Generated by Django 4.0 on 2022-02-21 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0038_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Chemistry', 'Chemistry'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Clothing and Textiles', 'Clothing and Textiles'), ('General Agriculture', 'General Agriculture'), ('Management-In-Living', 'Management-In-Living'), ('Jewellery', 'Jewellery'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Picture Making', 'Picture Making'), ('Social Studies', 'Social Studies'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Arabic', 'Arabic'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Animal Husbandry', 'Animal Husbandry'), ('Dagbani', 'Dagbani'), ('Woodwork', 'Woodwork'), ('French', 'French'), ('Gonja', 'Gonja'), ('Nzema', 'Nzema'), ('Biology', 'Biology'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Languages', 'Languages'), ('ICT (Elective)', 'ICT (Elective)'), ('Ewe', 'Ewe'), ('Auto Mechanics', 'Auto Mechanics'), ('Metalwork', 'Metalwork'), ('Dangme', 'Dangme'), ('Literature in English', 'Literature in English'), ('History', 'History'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Twi (Asante)', 'Twi (Asante)'), ('Integrated Science', 'Integrated Science'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Kasem', 'Kasem'), ('Dagaare', 'Dagaare'), ('Building Construction', 'Building Construction'), ('Geography', 'Geography'), ('Financial Accounting', 'Financial Accounting'), ('Economics', 'Economics'), ('Sculpture', 'Sculpture'), ('Leatherwork', 'Leatherwork'), ('Literature-in English', 'Literature-in English'), ('Graphic Design', 'Graphic Design'), ('Business Management', 'Business Management'), ('Electronics', 'Electronics'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Basketry', 'Basketry'), ('French OR Music', 'French OR Music'), ('Ceramics', 'Ceramics'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Ga', 'Ga'), ('Forestry', 'Forestry'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Music', 'Music'), ('Applied Electricity', 'Applied Electricity'), ('English Language', 'English Language'), ('Any one or two of the following', 'Any one or two of the following'), ('Fisheries', 'Fisheries'), ('Government', 'Government'), ('French or Music', 'French or Music'), ('Technical Drawing', 'Technical Drawing'), ('Textiles', 'Textiles'), ('Physics', 'Physics')], max_length=120),
        ),
    ]
