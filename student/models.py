import datetime
import os

from django.db import models

from accounts.models import User
from admission.models import StudentForms
from programme.models import Programme


class Student(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='student_profile',
                                   related_query_name='student',
                                   )
    admission_form = models.OneToOneField(StudentForms, related_name='student_admission_form',
                                          on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return str(self.profile)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ('id', 'profile')


class StudentProgrammeChoice(models.Model):
    first_choice = models.ForeignKey(Programme, related_name='first_choice', on_delete=models.CASCADE)
    second_choice = models.ForeignKey(Programme, related_name='second_choice', on_delete=models.CASCADE)
    third_choice = models.ForeignKey(Programme, related_name='third_choice', on_delete=models.CASCADE)
    student = models.OneToOneField(unique=True, to=Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'studentprogrammechoice'
        unique_together = ('first_choice', 'second_choice', 'student')


def upload_certificate_copy_to(instance, filename):
    return os.path.join('student', instance.name, instance.slug, 'certificate_copy', filename)


class AdmissionCertificate(models.Model):
    student = models.OneToOneField(Student, related_query_name='student', related_name='student',
                                   on_delete=models.CASCADE, unique=True)
    certificate_picture = models.FileField(
        upload_to=upload_certificate_copy_to,
        help_text='Include all the necessary(WASSCE, NOV/DEC, HND, SRN, Diploma Cert, etc) certificate in one pdf file'
    )

    class Meta:
        db_table = 'student_admission_exam_certificate'


class AdmissionExaminationTextChoice(models.TextChoices):
    PRIVATE_CANDIDATE = ('private candidate', 'Private Candidate')
    SCHOOL_CANDIDATE = ('school candidate', 'School Candidate')


EXAMINATION_YEAR_START = 1980


def examination_year_tuple():
    """ :return  iterable containing (actual value, human readable name) tuples. """
    return ((yr, yr) for yr in range(EXAMINATION_YEAR_START, datetime.date.today().year + 1))


class CertExamRecord(models.Model):
    certificate = models.ForeignKey(AdmissionCertificate, on_delete=models.CASCADE, related_name='certificate')
    subject = models.CharField(max_length=120)
    index_number = models.CharField(max_length=30, help_text='Examination number')
    examination_year = models.IntegerField(choices=examination_year_tuple())
    school = models.CharField(max_length=200, help_text='School Name', null=True, blank=True)
    Grade = models.CharField(max_length=3)
    examination_type = models.CharField(max_length=120,
                                        choices=AdmissionExaminationTextChoice.choices,
                                        default=AdmissionExaminationTextChoice.SCHOOL_CANDIDATE
                                        )

    class Meta:
        db_table = 'student_admission_exam_result'
