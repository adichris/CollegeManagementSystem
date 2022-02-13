# Generated by Django 4.0 on 2022-02-11 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0031_alter_student_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certexamrecord',
            name='examination_year',
            field=models.IntegerField(choices=[(2022, 2022), (2021, 2021), (2020, 2020), (2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981)]),
        ),
        migrations.AlterField(
            model_name='certexamrecord',
            name='grade',
            field=models.CharField(choices=[('A1', 'A1'), ('B2', 'B2'), ('B3', 'B3'), ('C4', 'C4'), ('C5', 'C5'), ('C6', 'C6'), ('D7', 'D7'), ('E8', 'E8'), ('F9', 'F9')], max_length=3),
        ),
        migrations.AlterField(
            model_name='certexamrecord',
            name='subject',
            field=models.CharField(choices=[('Chemistry', 'Chemistry'), ('Animal Husbandry', 'Animal Husbandry'), ('Biology', 'Biology'), ('Mathematics (Elective)', 'Mathematics (Elective)'), ('Dagaare', 'Dagaare'), ('Twi (Asante)', 'Twi (Asante)'), ('Crop Husbandry and Horticulture', 'Crop Husbandry and Horticulture'), ('History', 'History'), ('Economics', 'Economics'), ('Dagbani', 'Dagbani'), ('Typewriting (40wpm)', 'Typewriting (40wpm)'), ('Foods and Nutrition', 'Foods and Nutrition'), ('Arabic', 'Arabic'), ('Picture Making', 'Picture Making'), ('Islamic Religious Studies', 'Islamic Religious Studies'), ('Kasem', 'Kasem'), ('Applied Electricity', 'Applied Electricity'), ('Business Management', 'Business Management'), ('Electronics', 'Electronics'), ('French', 'French'), ('Sculpture', 'Sculpture'), ('Music', 'Music'), ('Building Construction', 'Building Construction'), ('Ceramics', 'Ceramics'), ('Geography', 'Geography'), ('General Knowledge-In-Art', 'General Knowledge-In-Art'), ('Ewe', 'Ewe'), ('Jewellery', 'Jewellery'), ('Twi (Akuapem)', 'Twi (Akuapem)'), ('Government', 'Government'), ('Management-In-Living', 'Management-In-Living'), ('Financial Accounting', 'Financial Accounting'), ('Any one or two of the following', 'Any one or two of the following'), ('Clothing and Textiles', 'Clothing and Textiles'), ('Languages', 'Languages'), ('Integrated Science', 'Integrated Science'), ('Clerical Office Duties', 'Clerical Office Duties'), ('Literature in English', 'Literature in English'), ('Dangme', 'Dangme'), ('Fisheries', 'Fisheries'), ('Woodwork', 'Woodwork'), ('Mathematics (Core)', 'Mathematics (Core)'), ('Textiles', 'Textiles'), ('Basketry', 'Basketry'), ('Nzema', 'Nzema'), ('ICT (Elective)', 'ICT (Elective)'), ('Physics', 'Physics'), ('General Agriculture', 'General Agriculture'), ('Metalwork', 'Metalwork'), ('Leatherwork', 'Leatherwork'), ('Ga', 'Ga'), ('Graphic Design', 'Graphic Design'), ('Gonja', 'Gonja'), ('Forestry', 'Forestry'), ('West Africa Traditional Religion', 'West Africa Traditional Religion'), ('French or Music', 'French or Music'), ('Auto Mechanics', 'Auto Mechanics'), ('Christian Religious Studies', 'Christian Religious Studies'), ('Principles of Cost Accounting', 'Principles of Cost Accounting'), ('Social Studies', 'Social Studies'), ('French OR Music', 'French OR Music'), ('English Language', 'English Language'), ('Literature-in English', 'Literature-in English'), ('Technical Drawing', 'Technical Drawing')], max_length=120),
        ),
        migrations.AlterField(
            model_name='studentpreviouseducation',
            name='from_year',
            field=models.IntegerField(choices=[(2022, 2022), (2021, 2021), (2020, 2020), (2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981)]),
        ),
        migrations.AlterField(
            model_name='studentpreviouseducation',
            name='to_year',
            field=models.IntegerField(choices=[(2022, 2022), (2021, 2021), (2020, 2020), (2019, 2019), (2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981)]),
        ),
    ]