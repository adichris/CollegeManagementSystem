# Generated by Django 4.0.2 on 2022-03-15 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0048_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Mathematics (Core)', 'Mathematics (Core)'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Sculpture', 'Sculpture'), ('English Language', 'English Language'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Arabic', 'Arabic'), ('Social Studies', 'Social Studies'), ('Animal Husbandry', 'Animal Husbandry'), ('Dagbani', 'Dagbani'), ('Applied Electricity', 'Applied Electricity'), ('Technical Drawing', 'Technical Drawing'), ('Twi (Asante)', 'Twi (Asante)'), ('Biology', 'Biology'), ('Picture Making', 'Picture Making'), ('Leatherwork', 'Leatherwork'), ('Nzema', 'Nzema'), ('Fisheries', 'Fisheries'), ('Jewellery', 'Jewellery'), ('ICT (Elective)', 'ICT (Elective)'), ('Business Management', 'Business Management'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('General Agriculture', 'General Agriculture'), ('Financial Accounting', 'Financial Accounting'), ('Management-In-Living', 'Management-In-Living'), ('Basketry', 'Basketry'), ('Ewe', 'Ewe'), ('Languages', 'Languages'), ('Economics', 'Economics'), ('Chemistry', 'Chemistry'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Forestry', 'Forestry'), ('Building Construction', 'Building Construction'), ('Any one or two of the following', 'Any one or two of the following'), ('Kasem', 'Kasem'), ('Integrated Science', 'Integrated Science'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('History', 'History'), ('Dangme', 'Dangme'), ('Geography', 'Geography'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Physics', 'Physics'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Textiles', 'Textiles'), ('Literature-in English', 'Literature-in English'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Government', 'Government'), ('French OR Music', 'French OR Music'), ('Dagaare', 'Dagaare'), ('Ceramics', 'Ceramics'), ('Auto Mechanics', 'Auto Mechanics'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Woodwork', 'Woodwork'), ('French', 'French'), ('Metalwork', 'Metalwork'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Ga', 'Ga'), ('Literature in English', 'Literature in English'), ('Graphic Design', 'Graphic Design'), ('Music', 'Music'), ('Electronics', 'Electronics'), ('Gonja', 'Gonja'), ('French or Music', 'French or Music')], max_length=120),
        ),
    ]