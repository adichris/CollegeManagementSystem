# Generated by Django 4.0.2 on 2022-03-19 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0056_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Electronics', 'Electronics'), ('Basketry', 'Basketry'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Nzema', 'Nzema'), ('Applied Electricity', 'Applied Electricity'), ('History', 'History'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Biology', 'Biology'), ('Integrated Science', 'Integrated Science'), ('French OR Music', 'French OR Music'), ('Chemistry', 'Chemistry'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Economics', 'Economics'), ('ICT (Elective)', 'ICT (Elective)'), ('Government', 'Government'), ('Ga', 'Ga'), ('Animal Husbandry', 'Animal Husbandry'), ('Arabic', 'Arabic'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Languages', 'Languages'), ('Dagaare', 'Dagaare'), ('Management-In-Living', 'Management-In-Living'), ('Ewe', 'Ewe'), ('Music', 'Music'), ('Leatherwork', 'Leatherwork'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Physics', 'Physics'), ('Fisheries', 'Fisheries'), ('General Agriculture', 'General Agriculture'), ('Any one or two of the following', 'Any one or two of the following'), ('Picture Making', 'Picture Making'), ('Social Studies', 'Social Studies'), ('Dagbani', 'Dagbani'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Sculpture', 'Sculpture'), ('French or Music', 'French or Music'), ('Graphic Design', 'Graphic Design'), ('English Language', 'English Language'), ('Forestry', 'Forestry'), ('Twi (Asante)', 'Twi (Asante)'), ('Textiles', 'Textiles'), ('Technical Drawing', 'Technical Drawing'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Literature-in English', 'Literature-in English'), ('French', 'French'), ('Ceramics', 'Ceramics'), ('Business Management', 'Business Management'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Dangme', 'Dangme'), ('Building Construction', 'Building Construction'), ('Geography', 'Geography'), ('Kasem', 'Kasem'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Auto Mechanics', 'Auto Mechanics'), ('Financial Accounting', 'Financial Accounting'), ('Woodwork', 'Woodwork'), ('Metalwork', 'Metalwork'), ('Literature in English', 'Literature in English'), ('Jewellery', 'Jewellery'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Gonja', 'Gonja')], max_length=120),
        ),
    ]