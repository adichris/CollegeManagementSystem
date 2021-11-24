import datetime
import os
from django.db import models

from accounts.models import User
from admission.models import StudentForms
from programme.models import Programme


class Student(models.Model):
    # add choice give field / programme
    profile = models.OneToOneField(User,
                                   on_delete=models.CASCADE,
                                   unique=True, related_name='student_profile',
                                   related_query_name='student',
                                   )
    admission_form = models.OneToOneField(StudentForms, related_name='student_admission_form',
                                          on_delete=models.CASCADE, unique=True)
    index_number = models.CharField(null=True, blank=True, max_length=60)

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
    student = models.OneToOneField(unique=True, to=Student, on_delete=models.CASCADE, related_name='programme_choices')

    class Meta:
        db_table = 'studentprogrammechoice'
        unique_together = ('first_choice', 'second_choice', 'student')

    def __str__(self):
        return str(self.student.admission_form.serial_number)


def upload_certificate_copy_to(instance, filename):
    return os.path.join('student', instance.name, instance.slug, 'certificate_copy', filename)


class AdmissionCertificate(models.Model):
    student = models.OneToOneField(Student, related_name='cert_student',
                                   on_delete=models.CASCADE, unique=True)
    certificate_picture = models.FileField(
        null=True,
        upload_to=upload_certificate_copy_to,
        help_text='Include all the necessary(WASSCE, NOV/DEC, HND, SRN, Diploma Cert, etc) certificate in one pdf file'
    )

    class Meta:
        db_table = 'student_admission_exam_certificate'

    def __str__(self):
        return str(self.student) + ' exam certificate'


class AdmissionExaminationTextChoice(models.TextChoices):
    PRIVATE_CANDIDATE = ('private candidate', 'Private Candidate')
    SCHOOL_CANDIDATE = ('school candidate', 'School Candidate')


EXAMINATION_YEAR_START = 1980
EXAMINATION_YEAR_END = datetime.date.today().year


class WaecGradeChoices(models.TextChoices):
    A = 'A', 'A'
    B = 'B', 'B'
    B2 = 'B2', 'B2'
    C = 'C', 'C'
    C2 = 'C2', 'C2'
    C3 = 'C3', 'C3'
    C4 = 'C4', 'C4'
    D = 'D', 'D'
    E8 = 'E8', 'E8'
    F9 = 'F9', 'F9'


def examination_year_tuple():
    """ :return  iterable containing (actual value, human readable name) tuples. """

    return tuple((yr, yr) for yr in range(EXAMINATION_YEAR_END, EXAMINATION_YEAR_START, -1))


class CertExamRecordManager(models.Manager):
    def get_for_certificate(self, certificate_id):
        return self.filter(certificate_id=certificate_id)


class CertExamRecord(models.Model):
    certificate = models.ForeignKey(AdmissionCertificate,
                                    on_delete=models.CASCADE,
                                    related_name='certificate_records',
                                    related_query_name='certificate_records',
                                    )
    subject = models.CharField(max_length=120)
    index_number = models.CharField(max_length=20, help_text='Examination number')
    examination_year = models.IntegerField(choices=examination_year_tuple())
    school = models.CharField(max_length=200, help_text='School Name', null=True, blank=True)
    grade = models.CharField(max_length=3, choices=WaecGradeChoices.choices)
    # TODO change grade to select field
    examination_type = models.CharField(max_length=120,
                                        choices=AdmissionExaminationTextChoice.choices,
                                        default=AdmissionExaminationTextChoice.SCHOOL_CANDIDATE
                                        )
    objects = CertExamRecordManager()

    class Meta:
        db_table = 'student_admission_exam_result'
        unique_together = ('certificate', 'examination_type', 'examination_year', 'subject')

    def __str__(self):
        return self.subject


class StudentPreviousEducation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='previous_education',
                                related_query_name='previous_education')
    school = models.CharField(max_length=200, help_text='Previous school name')
    region = models.CharField(max_length=200, help_text='Region the school is located')
    from_year = models.IntegerField(choices=examination_year_tuple())
    to_year = models.IntegerField(choices=examination_year_tuple())

    class Meta:
        db_table = 'studentpreviouseducation'
        verbose_name_plural = 'Student Previous Education'
        unique_together = (
            'student', 'school', 'to_year'
        )

    def __str__(self):
        return self.school
