# Generated by Django 4.0.2 on 2022-03-24 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0058_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Ceramics', 'Ceramics'), ('Languages', 'Languages'), ('Animal Husbandry', 'Animal Husbandry'), ('Woodwork', 'Woodwork'), ('Kasem', 'Kasem'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Forestry', 'Forestry'), ('Textiles', 'Textiles'), ('Financial Accounting', 'Financial Accounting'), ('Dangme', 'Dangme'), ('Chemistry', 'Chemistry'), ('Ewe', 'Ewe'), ('Technical Drawing', 'Technical Drawing'), ('Management-In-Living', 'Management-In-Living'), ('Dagbani', 'Dagbani'), ('Gonja', 'Gonja'), ('Jewellery', 'Jewellery'), ('Applied Electricity', 'Applied Electricity'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Literature in English', 'Literature in English'), ('Business Management', 'Business Management'), ('English Language', 'English Language'), ('Metalwork', 'Metalwork'), ('Social Studies', 'Social Studies'), ('Arabic', 'Arabic'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Dagaare', 'Dagaare'), ('French OR Music', 'French OR Music'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Integrated Science', 'Integrated Science'), ('Sculpture', 'Sculpture'), ('Music', 'Music'), ('General Agriculture', 'General Agriculture'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Literature-in English', 'Literature-in English'), ('Twi (Asante)', 'Twi (Asante)'), ('Auto Mechanics', 'Auto Mechanics'), ('History', 'History'), ('Geography', 'Geography'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Leatherwork', 'Leatherwork'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Basketry', 'Basketry'), ('ICT (Elective)', 'ICT (Elective)'), ('Electronics', 'Electronics'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Economics', 'Economics'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Biology', 'Biology'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Picture Making', 'Picture Making'), ('Government', 'Government'), ('Any one or two of the following', 'Any one or two of the following'), ('Physics', 'Physics'), ('French', 'French'), ('Building Construction', 'Building Construction'), ('Nzema', 'Nzema'), ('Ga', 'Ga'), ('Fisheries', 'Fisheries'), ('French or Music', 'French or Music'), ('Graphic Design', 'Graphic Design'), ('Foods and Nutrition', 'Foods and Nutrition')], max_length=120),
        ),
    ]