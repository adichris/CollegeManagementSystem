# Generated by Django 4.0 on 2022-02-13 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0033_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Twi (Akuapem)', 'Twi (Akuapem)'), ('Kasem', 'Kasem'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Animal Husbandry', 'Animal Husbandry'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Literature-in English', 'Literature-in English'), ('Biology', 'Biology'), ('Textiles', 'Textiles'), ('Electronics', 'Electronics'), ('Any one or two of the following', 'Any one or two of the following'), ('English Language', 'English Language'), ('Applied Electricity', 'Applied Electricity'), ('Basketry', 'Basketry'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Management-In-Living', 'Management-In-Living'), ('Auto Mechanics', 'Auto Mechanics'), ('ICT (Elective)', 'ICT (Elective)'), ('Social Studies', 'Social Studies'), ('Ga', 'Ga'), ('French or Music', 'French or Music'), ('Graphic Design', 'Graphic Design'), ('Music', 'Music'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Geography', 'Geography'), ('Gonja', 'Gonja'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Leatherwork', 'Leatherwork'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Government', 'Government'), ('Sculpture', 'Sculpture'), ('Dagaare', 'Dagaare'), ('French OR Music', 'French OR Music'), ('Nzema', 'Nzema'), ('Business Management', 'Business Management'), ('Clothing and Textiles', 'Clothing and Textiles'), ('French', 'French'), ('Dagbani', 'Dagbani'), ('Financial Accounting', 'Financial Accounting'), ('Languages', 'Languages'), ('Integrated Science', 'Integrated Science'), ('Woodwork', 'Woodwork'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Jewellery', 'Jewellery'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Ewe', 'Ewe'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Picture Making', 'Picture Making'), ('Fisheries', 'Fisheries'), ('Economics', 'Economics'), ('Dangme', 'Dangme'), ('Forestry', 'Forestry'), ('Building Construction', 'Building Construction'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Arabic', 'Arabic'), ('General Agriculture', 'General Agriculture'), ('Literature in English', 'Literature in English'), ('Ceramics', 'Ceramics'), ('Technical Drawing', 'Technical Drawing'), ('Twi (Asante)', 'Twi (Asante)'), ('Metalwork', 'Metalwork'), ('Chemistry', 'Chemistry'), ('Physics', 'Physics'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('History', 'History')], max_length=120),
        ),
    ]