# Generated by Django 4.0.2 on 2022-03-19 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0051_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Integrated Science', 'Integrated Science'), ('Any one or two of the following', 'Any one or two of the following'), ('Social Studies', 'Social Studies'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Leatherwork', 'Leatherwork'), ('Music', 'Music'), ('Business Management', 'Business Management'), ('ICT (Elective)', 'ICT (Elective)'), ('Nzema', 'Nzema'), ('Metalwork', 'Metalwork'), ('Jewellery', 'Jewellery'), ('Fisheries', 'Fisheries'), ('French', 'French'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Dagaare', 'Dagaare'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Ewe', 'Ewe'), ('Financial Accounting', 'Financial Accounting'), ('Animal Husbandry', 'Animal Husbandry'), ('English Language', 'English Language'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Building Construction', 'Building Construction'), ('Auto Mechanics', 'Auto Mechanics'), ('Graphic Design', 'Graphic Design'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Gonja', 'Gonja'), ('French or Music', 'French or Music'), ('Dagbani', 'Dagbani'), ('Picture Making', 'Picture Making'), ('Applied Electricity', 'Applied Electricity'), ('Kasem', 'Kasem'), ('Twi (Asante)', 'Twi (Asante)'), ('Dangme', 'Dangme'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Economics', 'Economics'), ('Electronics', 'Electronics'), ('Physics', 'Physics'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Chemistry', 'Chemistry'), ('Management-In-Living', 'Management-In-Living'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Ceramics', 'Ceramics'), ('Arabic', 'Arabic'), ('Literature in English', 'Literature in English'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Textiles', 'Textiles'), ('Biology', 'Biology'), ('Geography', 'Geography'), ('Woodwork', 'Woodwork'), ('Sculpture', 'Sculpture'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Technical Drawing', 'Technical Drawing'), ('Ga', 'Ga'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('General Agriculture', 'General Agriculture'), ('Forestry', 'Forestry'), ('Literature-in English', 'Literature-in English'), ('French OR Music', 'French OR Music'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Languages', 'Languages'), ('History', 'History'), ('Basketry', 'Basketry'), ('Government', 'Government'), ('Mathematics (Core)', 'Mathematics (Core)')], max_length=120),
        ),
    ]