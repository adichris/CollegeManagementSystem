# Generated by Django 4.1 on 2022-08-21 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0062_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Picture Making', 'Picture Making'), ('History', 'History'), ('English Language', 'English Language'), ('Applied Electricity', 'Applied Electricity'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Animal Husbandry', 'Animal Husbandry'), ('Literature in English', 'Literature in English'), ('French or Music', 'French or Music'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Ga', 'Ga'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Literature-in English', 'Literature-in English'), ('Leatherwork', 'Leatherwork'), ('Kasem', 'Kasem'), ('Geography', 'Geography'), ('Economics', 'Economics'), ('French', 'French'), ('Nzema', 'Nzema'), ('Business Management', 'Business Management'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Fisheries', 'Fisheries'), ('Technical Drawing', 'Technical Drawing'), ('Textiles', 'Textiles'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Any one or two of the following', 'Any one or two of the following'), ('Languages', 'Languages'), ('Music', 'Music'), ('Graphic Design', 'Graphic Design'), ('Electronics', 'Electronics'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Integrated Science', 'Integrated Science'), ('Dagaare', 'Dagaare'), ('Auto Mechanics', 'Auto Mechanics'), ('Gonja', 'Gonja'), ('Basketry', 'Basketry'), ('Jewellery', 'Jewellery'), ('Sculpture', 'Sculpture'), ('Biology', 'Biology'), ('Social Studies', 'Social Studies'), ('Forestry', 'Forestry'), ('Dangme', 'Dangme'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Twi (Asante)', 'Twi (Asante)'), ('Building Construction', 'Building Construction'), ('Ceramics', 'Ceramics'), ('Government', 'Government'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Ewe', 'Ewe'), ('Metalwork', 'Metalwork'), ('General Agriculture', 'General Agriculture'), ('Management-In-Living', 'Management-In-Living'), ('Physics', 'Physics'), ('Woodwork', 'Woodwork'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Chemistry', 'Chemistry'), ('ICT (Elective)', 'ICT (Elective)'), ('Arabic', 'Arabic'), ('Dagbani', 'Dagbani'), ('French OR Music', 'French OR Music'), ('Financial Accounting', 'Financial Accounting'), ('Mathematics (Elective)', 'Mathematics (Elective)')], max_length=120),
        ),
    ]
