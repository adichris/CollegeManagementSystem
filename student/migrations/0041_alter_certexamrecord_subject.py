# Generated by Django 4.0.2 on 2022-03-03 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0040_alter_certexamrecord_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('English Language', 'English Language'), ('Basketry', 'Basketry'), ('Applied Electricity', 'Applied Electricity'), ('Management-In-Living', 'Management-In-Living'), ('French or Music', 'French or Music'), ('Arabic', 'Arabic'), ('Metalwork', 'Metalwork'), ('Building Construction', 'Building Construction'), ('Geography', 'Geography'), ('Leatherwork', 'Leatherwork'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Any one or two of the following', 'Any one or two of the following'), ('Ceramics', 'Ceramics'), ('Music', 'Music'), ('Literature-in English', 'Literature-in English'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Electronics', 'Electronics'), ('French', 'French'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Picture Making', 'Picture Making'), ('Government', 'Government'), ('Integrated Science', 'Integrated Science'), ('French OR Music', 'French OR Music'), ('Gonja', 'Gonja'), ('Kasem', 'Kasem'), ('Animal Husbandry', 'Animal Husbandry'), ('Graphic Design', 'Graphic Design'), ('Business Management', 'Business Management'), ('Languages', 'Languages'), ('Jewellery', 'Jewellery'), ('Physics', 'Physics'), ('Financial Accounting', 'Financial Accounting'), ('Dagbani', 'Dagbani'), ('ICT (Elective)', 'ICT (Elective)'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Auto Mechanics', 'Auto Mechanics'), ('Textiles', 'Textiles'), ('Woodwork', 'Woodwork'), ('Literature in English', 'Literature in English'), ('Christian Religious Studies', 'Christian Religious Studies'), ('General Agriculture', 'General Agriculture'), ('History', 'History'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('Nzema', 'Nzema'), ('Chemistry', 'Chemistry'), ('Biology', 'Biology'), ('Twi (Asante)', 'Twi (Asante)'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Dangme', 'Dangme'), ('Ga', 'Ga'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Dagaare', 'Dagaare'), ('Technical Drawing', 'Technical Drawing'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Fisheries', 'Fisheries'), ('Sculpture', 'Sculpture'), ('Economics', 'Economics'), ('Social Studies', 'Social Studies'), ('Forestry', 'Forestry'), ('Ewe', 'Ewe')], max_length=120),
        ),
    ]
