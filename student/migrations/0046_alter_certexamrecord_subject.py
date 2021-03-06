# Generated by Django 4.0.2 on 2022-03-15 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0045_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Woodwork', 'Woodwork'), ('Gonja', 'Gonja'), ('Jewellery', 'Jewellery'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Metalwork', 'Metalwork'), ('Leatherwork', 'Leatherwork'), ('History', 'History'), ('French', 'French'), ('Dagbani', 'Dagbani'), ('Physics', 'Physics'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Any one or two of the following', 'Any one or two of the following'), ('Nzema', 'Nzema'), ('Animal Husbandry', 'Animal Husbandry'), ('Basketry', 'Basketry'), ('Dagaare', 'Dagaare'), ('Literature in English', 'Literature in English'), ('French or Music', 'French or Music'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Sculpture', 'Sculpture'), ('Ga', 'Ga'), ('Kasem', 'Kasem'), ('General Agriculture', 'General Agriculture'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Literature-in English', 'Literature-in English'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Electronics', 'Electronics'), ('Chemistry', 'Chemistry'), ('Integrated Science', 'Integrated Science'), ('ICT (Elective)', 'ICT (Elective)'), ('Picture Making', 'Picture Making'), ('Applied Electricity', 'Applied Electricity'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Languages', 'Languages'), ('French OR Music', 'French OR Music'), ('Ceramics', 'Ceramics'), ('Auto Mechanics', 'Auto Mechanics'), ('Government', 'Government'), ('Technical Drawing', 'Technical Drawing'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Geography', 'Geography'), ('Social Studies', 'Social Studies'), ('Twi (Asante)', 'Twi (Asante)'), ('Biology', 'Biology'), ('Music', 'Music'), ('Dangme', 'Dangme'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Ewe', 'Ewe'), ('Economics', 'Economics'), ('Graphic Design', 'Graphic Design'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Financial Accounting', 'Financial Accounting'), ('English Language', 'English Language'), ('Textiles', 'Textiles'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Fisheries', 'Fisheries'), ('Arabic', 'Arabic'), ('Management-In-Living', 'Management-In-Living'), ('Building Construction', 'Building Construction'), ('Business Management', 'Business Management'), ('Forestry', 'Forestry')], max_length=120),
        ),
    ]
