# Generated by Django 4.0 on 2022-02-21 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0039_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Literature in English', 'Literature in English'), ('Arabic', 'Arabic'), ('Any one or two of the following', 'Any one or two of the following'), ('Textiles', 'Textiles'), ('ICT (Elective)', 'ICT (Elective)'), ('Basketry', 'Basketry'), ('Social Studies', 'Social Studies'), ('Languages', 'Languages'), ('Building Construction', 'Building Construction'), ('Government', 'Government'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Biology', 'Biology'), ('Geography', 'Geography'), ('Technical Drawing', 'Technical Drawing'), ('Ga', 'Ga'), ('Graphic Design', 'Graphic Design'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Sculpture', 'Sculpture'), ('Nzema', 'Nzema'), ('Foods and Nutrition', 'Foods and Nutrition'), ('General Agriculture', 'General Agriculture'), ('Ceramics', 'Ceramics'), ('Dangme', 'Dangme'), ('Metalwork', 'Metalwork'), ('Picture Making', 'Picture Making'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Dagbani', 'Dagbani'), ('Fisheries', 'Fisheries'), ('French OR Music', 'French OR Music'), ('Leatherwork', 'Leatherwork'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Ewe', 'Ewe'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('English Language', 'English Language'), ('Management-In-Living', 'Management-In-Living'), ('Animal Husbandry', 'Animal Husbandry'), ('Twi (Asante)', 'Twi (Asante)'), ('Applied Electricity', 'Applied Electricity'), ('Integrated Science', 'Integrated Science'), ('French', 'French'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Chemistry', 'Chemistry'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Economics', 'Economics'), ('French or Music', 'French or Music'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Gonja', 'Gonja'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Physics', 'Physics'), ('Business Management', 'Business Management'), ('Woodwork', 'Woodwork'), ('Jewellery', 'Jewellery'), ('Music', 'Music'), ('History', 'History'), ('Literature-in English', 'Literature-in English'), ('Financial Accounting', 'Financial Accounting'), ('Kasem', 'Kasem'), ('Electronics', 'Electronics'), ('Forestry', 'Forestry'), ('Dagaare', 'Dagaare'), ('Auto Mechanics', 'Auto Mechanics')], max_length=120),
        ),
    ]
